from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils.text import slugify
from django.contrib.auth.models import User
import json
import datetime

from .igdb_service import IGDBService
from .models import Review, Genre
from developer.models import Developer
from publisher.models import Publisher
from .management.commands.populate_reviews import Command as PopulateCommand


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def populate_reviews_interface(request):
    """Main interface for populating reviews"""
    if request.method == 'POST':
        search_term = request.POST.get('search', '')
        limit = int(request.POST.get('limit', 50))

        # Get games from IGDB
        igdb_service = IGDBService()
        if search_term:
            games = igdb_service.search_games_with_platforms(search_term, limit=limit)
        else:
            games = igdb_service.search_games_with_platforms('', limit=limit)

        # Format games for template
        formatted_games = []
        for idx, game in enumerate(games, 1):
            title = game.get('name', 'Unknown')
            year = None
            if 'release_dates' in game and game['release_dates']:
                try:
                    timestamp = game['release_dates'][0]['date']
                    year = datetime.datetime.fromtimestamp(timestamp).year
                except Exception:
                    year = 'Unknown'
            platforms = ', '.join([p.get('name', 'Unknown') for p in game.get('platforms', [])])

            formatted_games.append({
                'index': idx,
                'title': title,
                'year': year,
                'platforms': platforms,
                'summary': game.get('summary', ''),
                'raw_data': json.dumps(game)  # Store as JSON string for hidden input
            })

        return render(request, 'reviews/populate_reviews.html', {
            'games': formatted_games,
            'search_term': search_term,
            'limit': limit
        })

    return render(request, 'reviews/populate_reviews.html')


@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def create_reviews_from_selection(request):
    """Create reviews from selected games"""
    try:
        selected_games_data = request.POST.getlist('selected_games')
        review_scores = request.POST.getlist('review_scores')

        if not selected_games_data:
            messages.error(request, 'No games selected')
            return redirect('reviews:populate_interface')

        created_reviews = 0
        populate_command = PopulateCommand()

        with transaction.atomic():
            for i, game_json in enumerate(selected_games_data):
                try:
                    game = json.loads(game_json)
                    review_score = float(review_scores[i]) if i < len(review_scores) else 5.0

                    title = game.get('name')
                    slug = slugify(title)
                    description = game.get('summary', '')
                    release_date = None
                    if 'release_dates' in game and game['release_dates']:
                        try:
                            timestamp = game['release_dates'][0]['date']
                            release_date = datetime.datetime.fromtimestamp(timestamp).date()
                        except Exception:
                            release_date = None

                    # Handle developer
                    developer_obj = None
                    if game.get('developers'):
                        dev_data = game['developers'][0]
                        logo_url = dev_data.get('logo_url', '')
                        if logo_url and logo_url.startswith('//'):
                            logo_url = 'https:' + logo_url
                        cloudinary_logo_id = populate_command.upload_developer_logo_to_cloudinary(logo_url, dev_data['name'])
                        developer_obj, _ = Developer.objects.get_or_create(
                            name=dev_data['name'],
                            defaults={
                                'description': dev_data.get('description', ''),
                                'website': dev_data.get('website', ''),
                                'founded_year': dev_data.get('founded_year') or None,
                                'logo': cloudinary_logo_id if cloudinary_logo_id else logo_url
                            }
                        )

                    # Handle publisher
                    publisher_obj = None
                    if game.get('publishers'):
                        pub_data = game['publishers'][0]
                        logo_url = pub_data.get('logo_url', '')
                        if logo_url and logo_url.startswith('//'):
                            logo_url = 'https:' + logo_url
                        cloudinary_logo_id = populate_command.upload_publisher_logo_to_cloudinary(logo_url, pub_data['name'])
                        publisher_obj, _ = Publisher.objects.get_or_create(
                            name=pub_data['name'],
                            defaults={
                                'description': pub_data.get('description', ''),
                                'website': pub_data.get('website', ''),
                                'founded_year': pub_data.get('founded_year') or None,
                                'logo': cloudinary_logo_id if cloudinary_logo_id else logo_url
                            }
                        )

                    # Create review if both developer and publisher exist
                    if developer_obj and publisher_obj:
                        user = User.objects.order_by('?').first()

                        # Generate AI review
                        ai_review_text = populate_command.generate_ai_review(title)
                        review_text = ai_review_text if ai_review_text else f"Auto-generated review for {title}."
                        review_date = datetime.datetime.now()

                        # Download and upload cover image
                        cover_url = game.get('cover_url', '')
                        if cover_url.startswith('//'):
                            cover_url = 'https:' + cover_url
                        cloudinary_id = populate_command.upload_cover_to_cloudinary(cover_url, title)
                        featured_image = cloudinary_id if cloudinary_id else 'placeholder'

                        review, created = Review.objects.get_or_create(
                            title=title,
                            slug=slug,
                            defaults={
                                'publisher': publisher_obj,
                                'developer': developer_obj,
                                'description': description,
                                'release_date': release_date or datetime.date.today(),
                                'review_score': review_score,
                                'review_text': review_text,
                                'reviewed_by': user,
                                'review_date': review_date,
                                'featured_image': featured_image,
                                'is_featured': False,
                                'is_published': True
                            }
                        )

                        # Add genres to review
                        genre_objs = []
                        for genre in game.get('genres', []):
                            genre_name = genre.get('name')
                            if genre_name:
                                genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                                genre_objs.append(genre_obj)
                        if genre_objs:
                            review.genres.set(genre_objs)

                        if created:
                            created_reviews += 1

                except Exception as e:
                    messages.error(request, f'Error processing {title}: {str(e)}')
                    continue

        messages.success(request, f'Successfully created {created_reviews} reviews')
        return redirect('reviews:populate_interface')

    except Exception as e:
        messages.error(request, f'Error creating reviews: {str(e)}')
        return redirect('reviews:populate_interface')
