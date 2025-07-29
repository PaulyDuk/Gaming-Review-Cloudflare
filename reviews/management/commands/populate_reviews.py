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
    def upload_developer_logo_to_cloudinary(self, logo_url, developer_name):
        """Download developer logo and upload to Cloudinary, return public_id or None"""
        import requests
        import tempfile
        from cloudinary.uploader import upload
        import os
        if not logo_url:
            return None
        try:
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            try:
                public_id = f"developer_logos/{developer_name.lower().replace(' ', '_')}"
                result = upload(
                    temp_file_path,
                    public_id=public_id,
                    folder="developer_logos",
                    overwrite=True,
                    resource_type="image"
                )
                return result['public_id']
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to upload developer logo for {developer_name}: {str(e)}"))
            return None

    def upload_publisher_logo_to_cloudinary(self, logo_url, publisher_name):
        """Download publisher logo and upload to Cloudinary, return public_id or None"""
        import requests
        import tempfile
        from cloudinary.uploader import upload
        import os
        if not logo_url:
            return None
        try:
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            try:
                public_id = f"publisher_logos/{publisher_name.lower().replace(' ', '_')}"
                result = upload(
                    temp_file_path,
                    public_id=public_id,
                    folder="publisher_logos",
                    overwrite=True,
                    resource_type="image"
                )
                return result['public_id']
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to upload publisher logo for {publisher_name}: {str(e)}"))
            return None
    def upload_cover_to_cloudinary(self, cover_url, game_title):
        """Download cover image and upload to Cloudinary, return public_id or None"""
        import requests
        import tempfile
        from cloudinary.uploader import upload
        import os
        if not cover_url:
            return None
        try:
            response = requests.get(cover_url, timeout=10)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            try:
                public_id = f"game_covers/{game_title.lower().replace(' ', '_')}"
                result = upload(
                    temp_file_path,
                    public_id=public_id,
                    folder="game_covers",
                    overwrite=True,
                    resource_type="image"
                )
                return result['public_id']
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to upload cover for {game_title}: {str(e)}"))
            return None
    help = 'Populate reviews, developers, and publishers from IGDB API'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=50, help='Number of games to process (default: 50)')
        parser.add_argument('--search', type=str, help='Search for a specific game name')

    def handle(self, *args, **options):
        limit = options['limit']
        search = options.get('search')
        self.stdout.write(self.style.SUCCESS(f'Starting IGDB review population (limit: {limit}, search: {search})'))
        igdb_service = IGDBService()

        if search:
            games = igdb_service.search_games_with_platforms(search, limit=limit)
        else:
            games = igdb_service.search_games_with_platforms('', limit=limit)

        if not games:
            self.stdout.write(self.style.WARNING('No games found matching your search.'))
            return

        # List all matching games with details
        self.stdout.write(self.style.SUCCESS('Matching games:'))
        for idx, game in enumerate(games, 1):
            title = game.get('name', 'Unknown')
            # Get first release year
            year = None
            if 'release_dates' in game and game['release_dates']:
                try:
                    timestamp = game['release_dates'][0]['date']
                    year = datetime.datetime.fromtimestamp(timestamp).year
                except Exception:
                    year = 'Unknown'
            platforms = ', '.join([p.get('name', 'Unknown') for p in game.get('platforms', [])])
            self.stdout.write(f"[{idx}] {title} | Year: {year} | Platforms: {platforms}")

        # Prompt user to select games to add
        self.stdout.write(self.style.WARNING('Enter the numbers of the games to add, separated by commas (e.g. 1,3):'))
        selection = input('Selection: ')
        selected_indices = set()
        for part in selection.split(','):
            try:
                selected_indices.add(int(part.strip()))
            except ValueError:
                continue

        created_reviews = 0
        with transaction.atomic():
            for idx, game in enumerate(games, 1):
                if idx not in selected_indices:
                    continue
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
                    cloudinary_logo_id = self.upload_developer_logo_to_cloudinary(logo_url, dev_data['name'])
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
                    cloudinary_logo_id = self.upload_publisher_logo_to_cloudinary(logo_url, pub_data['name'])
                    publisher_obj, _ = Publisher.objects.get_or_create(
                        name=pub_data['name'],
                        defaults={
                            'description': pub_data.get('description', ''),
                            'website': pub_data.get('website', ''),
                            'founded_year': pub_data.get('founded_year') or None,
                            'logo': cloudinary_logo_id if cloudinary_logo_id else logo_url
                        }
                    )

                # Only create review if both developer and publisher exist
                if developer_obj and publisher_obj:
                    user = User.objects.order_by('?').first()
                    review_score = round(random.uniform(6, 10), 1)
                    review_text = f"Auto-generated review for {title}."
                    review_date = datetime.datetime.now()

                    # Download and upload cover image
                    cover_url = game.get('cover_url', '')
                    if cover_url.startswith('//'):
                        cover_url = 'https:' + cover_url
                    cloudinary_id = self.upload_cover_to_cloudinary(cover_url, title)
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
                    if created:
                        created_reviews += 1
                        self.stdout.write(self.style.SUCCESS(f'✓ Created review: {title}'))
                    else:
                        self.stdout.write(f'- Exists: {title}')
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped: {title} (missing developer or publisher)'))

        self.stdout.write(self.style.SUCCESS(f'Total reviews created: {created_reviews}'))
