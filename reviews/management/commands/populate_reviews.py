from django.core.management.base import BaseCommand
from django.db import transaction
from reviews.models import Review
from developer.models import Developer
from publisher.models import Publisher
from reviews.igdb_service import IGDBService
from django.utils.text import slugify
from django.contrib.auth.models import User
import random
import datetime

class Command(BaseCommand):
    help = 'Populate reviews, developers, and publishers from IGDB API'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10, help='Number of games to process (default: 10)')
        parser.add_argument('--search', type=str, help='Search for a specific game name')

    def handle(self, *args, **options):
        limit = options['limit']
        search = options.get('search')
        self.stdout.write(self.style.SUCCESS(f'Starting IGDB review population (limit: {limit}, search: {search})'))
        igdb_service = IGDBService()

        if search:
            games = igdb_service.search_games_with_platforms(search, limit=1)
        else:
            games = igdb_service.search_games_with_platforms('', limit=limit)

        created_reviews = 0
        with transaction.atomic():
            for game in games:
                title = game.get('name')
                slug = slugify(title)
                description = game.get('summary', '')
                release_date = None
                if 'release_dates' in game and game['release_dates']:
                    # Use first release date
                    try:
                        timestamp = game['release_dates'][0]['date']
                        release_date = datetime.datetime.fromtimestamp(timestamp).date()
                    except Exception:
                        release_date = None
                genre = game['genres'][0]['name'] if game.get('genres') else 'Other'
                console = game['platforms'][0]['name'] if game.get('platforms') else 'Other'

                # Handle developer
                developer_obj = None
                if game.get('developers'):
                    dev_data = game['developers'][0]
                    developer_obj, _ = Developer.objects.get_or_create(
                        name=dev_data['name'],
                        defaults={
                            'description': dev_data.get('description', ''),
                            'website': dev_data.get('website', ''),
                            'founded_year': dev_data.get('founded_year') or None,
                            'logo': dev_data.get('logo_url', '')
                        }
                    )

                # Handle publisher
                publisher_obj = None
                if game.get('publishers'):
                    pub_data = game['publishers'][0]
                    publisher_obj, _ = Publisher.objects.get_or_create(
                        name=pub_data['name'],
                        defaults={
                            'description': pub_data.get('description', ''),
                            'website': pub_data.get('website', ''),
                            'founded_year': pub_data.get('founded_year') or None,
                            'logo': pub_data.get('logo_url', '')
                        }
                    )

                # Pick a random user for reviewed_by
                user = User.objects.order_by('?').first()
                review_score = round(random.uniform(6, 10), 1)
                review_text = f"Auto-generated review for {title}."
                review_date = datetime.datetime.now()

                # Create review
                review, created = Review.objects.get_or_create(
                    title=title,
                    slug=slug,
                    defaults={
                        'publisher': publisher_obj,
                        'developer': developer_obj,
                        'genre': genre,
                        'console': console,
                        'description': description,
                        'release_date': release_date or datetime.date.today(),
                        'review_score': review_score,
                        'review_text': review_text,
                        'reviewed_by': user,
                        'review_date': review_date,
                        'featured_image': 'placeholder',
                        'is_featured': False,
                        'is_published': True
                    }
                )
                if created:
                    created_reviews += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created review: {title}'))
                else:
                    self.stdout.write(f'- Exists: {title}')

        self.stdout.write(self.style.SUCCESS(f'Total reviews created: {created_reviews}'))
