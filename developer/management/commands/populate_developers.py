from django.core.management.base import BaseCommand
from django.db import transaction
from developer.models import Developer
from reviews.igdb_service import IGDBService
import requests
from cloudinary.uploader import upload
import tempfile
import os


class Command(BaseCommand):
    help = 'Populate developer database with information from IGDB API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Number of popular games to fetch developers from (default: 100)'
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing developers with IGDB data'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        update_existing = options['update_existing']

        self.stdout.write(
            self.style.SUCCESS(f'Starting IGDB developer population (limit: {limit})')
        )

        try:
            igdb_service = IGDBService()

            # Get popular games to extract developers from
            developers_data = self.fetch_developers_from_popular_games(
                igdb_service, limit
            )

            # Save developers to database
            created_count, updated_count = self.save_developers(
                developers_data, update_existing
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed developers:\n'
                    f'- Created: {created_count}\n'
                    f'- Updated: {updated_count}\n'
                    f'- Total unique developers found: {len(developers_data)}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )

    def fetch_developers_from_popular_games(self, igdb_service, limit):
        """Fetch developers from popular games"""
        # Use a list of popular games to extract developers from
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

        developers_dict = {}

        # Limit the number of games we process
        games_to_process = popular_games[:min(limit // 5, len(popular_games))]

        for game_name in games_to_process:
            try:
                self.stdout.write(f'Fetching developers from: {game_name}')
                game_data = igdb_service.get_game_platforms_by_name(game_name)

                if game_data and 'developers' in game_data:
                    for developer in game_data['developers']:
                        dev_name = developer.get('name', '').strip()
                        if dev_name and dev_name not in developers_dict:
                            developers_dict[dev_name] = {
                                'name': dev_name,
                                'description': developer.get('description', ''),
                                'website': developer.get('website', ''),
                                'founded_year': developer.get('founded_year') if developer.get('founded_year') else None,
                                'igdb_id': developer.get('id'),
                                'logo_url': developer.get('logo_url', '')
                            }
                            self.stdout.write(f'Found developer: {dev_name}')

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f'Error fetching developers from {game_name}: {str(e)}'
                    )
                )
                continue

        return list(developers_dict.values())

    def download_and_save_logo(self, logo_url, developer_name):
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
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f'Failed to download logo for {developer_name}: {str(e)}'
                )
            )
            return None

    def save_developers(self, developers_data, update_existing):
        """Save developers to database"""
        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for dev_data in developers_data:
                try:
                    developer, created = Developer.objects.get_or_create(
                        name=dev_data['name'],
                        defaults={
                            'description': dev_data['description'],
                            'website': dev_data['website'],
                            'founded_year': dev_data['founded_year'],
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {developer.name}')
                        )

                        # Download and set logo for new developers
                        if dev_data.get('logo_url'):
                            self.stdout.write(f'Downloading logo for {developer.name}...')
                            logo_public_id = self.download_and_save_logo(
                                dev_data['logo_url'],
                                developer.name
                            )
                            if logo_public_id:
                                developer.logo = logo_public_id
                                developer.save()
                                self.stdout.write(f'✓ Logo saved for {developer.name}')

                    elif update_existing:
                        # Update existing developer with IGDB data
                        updated = False
                        if dev_data['description'] and not developer.description:
                            developer.description = dev_data['description']
                            updated = True
                        if dev_data['website'] and not developer.website:
                            developer.website = dev_data['website']
                            updated = True
                        if dev_data['founded_year'] and not developer.founded_year:
                            developer.founded_year = dev_data['founded_year']
                            updated = True

                        # Update logo if developer doesn't have one
                        if (dev_data.get('logo_url') and
                                (not developer.logo or developer.logo == 'placeholder')):
                            self.stdout.write(f'Downloading logo for {developer.name}...')
                            logo_public_id = self.download_and_save_logo(
                                dev_data['logo_url'],
                                developer.name
                            )
                            if logo_public_id:
                                developer.logo = logo_public_id
                                updated = True
                                self.stdout.write(f'✓ Logo updated for {developer.name}')

                        if updated:
                            developer.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'↻ Updated: {developer.name}')
                            )
                        else:
                            self.stdout.write(f'- Skipped: {developer.name} (no new data)')
                    else:
                        self.stdout.write(f'- Exists: {developer.name}')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error saving developer {dev_data["name"]}: {str(e)}'
                        )
                    )

        return created_count, updated_count
