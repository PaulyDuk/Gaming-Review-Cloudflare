from django.core.management.base import BaseCommand
from django.db import transaction
from publisher.models import Publisher
from reviews.igdb_service import IGDBService
import json
import requests
from django.core.files.base import ContentFile
from cloudinary.uploader import upload
import tempfile
import os


class Command(BaseCommand):
    help = 'Populate publisher database with information from IGDB API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Number of popular games to fetch publishers from (default: 100)'
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing publishers with IGDB data'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        update_existing = options['update_existing']

        self.stdout.write(
            self.style.SUCCESS(f'Starting IGDB publisher population (limit: {limit})')
        )

        try:
            igdb_service = IGDBService()

            # Get popular games to extract publishers from
            publishers_data = self.fetch_publishers_from_popular_games(
                igdb_service, limit
            )

            # Save publishers to database
            created_count, updated_count = self.save_publishers(
                publishers_data, update_existing
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed publishers:\n'
                    f'- Created: {created_count}\n'
                    f'- Updated: {updated_count}\n'
                    f'- Total unique publishers found: {len(publishers_data)}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )

    def fetch_publishers_from_popular_games(self, igdb_service, limit):
        """Fetch publishers from popular games"""
        # Use a list of popular games to extract publishers from
        popular_games = [
            "God of War", "The Last of Us", "Horizon Zero Dawn",
            "Spider-Man", "Ghost of Tsushima", "Uncharted 4",
            "The Witcher 3", "Red Dead Redemption 2", "Grand Theft Auto V",
            "Dark Souls 3", "Cyberpunk 2077", "The Elder Scrolls V",
            "Call of Duty", "Battlefield", "Assassin's Creed", "FIFA",
            "Minecraft", "Fortnite", "League of Legends", "Dota 2",
            "Counter-Strike", "Overwatch", "Halo", "Zelda",
            "Mario", "Sekiro", "Bloodborne", "Elden Ring"
        ]

        publishers_dict = {}

        # Limit the number of games we process
        games_to_process = popular_games[:min(limit // 5, len(popular_games))]

        for game_name in games_to_process:
            try:
                self.stdout.write(f'Fetching publishers from: {game_name}')
                game_data = igdb_service.get_game_platforms_by_name(game_name)

                if game_data and 'publishers' in game_data:
                    for publisher in game_data['publishers']:
                        pub_name = publisher.get('name', '').strip()
                        if pub_name and pub_name not in publishers_dict:
                            publishers_dict[pub_name] = {
                                'name': pub_name,
                                'description': publisher.get('description', ''),
                                'website': publisher.get('website', ''),
                                'founded_year': publisher.get('founded_year') if publisher.get('founded_year') else None,
                                'igdb_id': publisher.get('id'),
                                'logo_url': publisher.get('logo_url', '')
                            }
                            self.stdout.write(f'Found publisher: {pub_name}')

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f'Error fetching publishers from {game_name}: {str(e)}'
                    )
                )
                continue

        return list(publishers_dict.values())

    def download_and_save_logo(self, logo_url, publisher_name):
        """Download logo from URL and save to Cloudinary"""
        if not logo_url:
            return None

        try:
            # Download the image
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()

            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            try:
                # Upload to Cloudinary with a clean public_id
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
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f'Failed to download logo for {publisher_name}: {str(e)}'
                )
            )
            return None

    def save_publishers(self, publishers_data, update_existing):
        """Save publishers to database"""
        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for pub_data in publishers_data:
                try:
                    publisher, created = Publisher.objects.get_or_create(
                        name=pub_data['name'],
                        defaults={
                            'description': pub_data['description'],
                            'website': pub_data['website'],
                            'founded_year': pub_data['founded_year'],
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {publisher.name}')
                        )

                        # Download and set logo for new publishers
                        if pub_data.get('logo_url'):
                            self.stdout.write(f'Downloading logo for {publisher.name}...')
                            logo_public_id = self.download_and_save_logo(
                                pub_data['logo_url'],
                                publisher.name
                            )
                            if logo_public_id:
                                publisher.logo = logo_public_id
                                publisher.save()
                                self.stdout.write(f'✓ Logo saved for {publisher.name}')

                    elif update_existing:
                        # Update existing publisher with IGDB data
                        updated = False
                        if pub_data['description'] and not publisher.description:
                            publisher.description = pub_data['description']
                            updated = True
                        if pub_data['website'] and not publisher.website:
                            publisher.website = pub_data['website']
                            updated = True
                        if pub_data['founded_year'] and not publisher.founded_year:
                            publisher.founded_year = pub_data['founded_year']
                            updated = True

                        # Update logo if publisher doesn't have one
                        if (pub_data.get('logo_url') and
                                (not publisher.logo or publisher.logo == 'placeholder')):
                            self.stdout.write(f'Downloading logo for {publisher.name}...')
                            logo_public_id = self.download_and_save_logo(
                                pub_data['logo_url'],
                                publisher.name
                            )
                            if logo_public_id:
                                publisher.logo = logo_public_id
                                updated = True
                                self.stdout.write(f'✓ Logo updated for {publisher.name}')

                        if updated:
                            publisher.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'↻ Updated: {publisher.name}')
                            )
                        else:
                            self.stdout.write(f'- Skipped: {publisher.name} (no new data)')
                    else:
                        self.stdout.write(f'- Exists: {publisher.name}')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error saving publisher {pub_data["name"]}: {str(e)}'
                        )
                    )

        return created_count, updated_count
