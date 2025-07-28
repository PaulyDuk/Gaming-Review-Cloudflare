from django.core.management.base import BaseCommand
from django.db import transaction
from developer.models import Developer
from reviews.igdb_service import IGDBService
import json


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
        wrapper = igdb_service.initialize_wrapper()
        
        # Query for popular games with high rating and release dates
        query_string = (
            f'fields involved_companies.company.name, '
            f'involved_companies.company.description, '
            f'involved_companies.company.websites.url, '
            f'involved_companies.company.websites.category, '
            f'involved_companies.company.start_date, '
            f'involved_companies.developer; '
            f'where rating > 70 & rating_count > 10; '
            f'sort rating desc; '
            f'limit {limit};'
        )

        try:
            byte_array = wrapper.api_request('games', query_string)
            games = json.loads(byte_array)
            
            developers_dict = {}
            
            for game in games:
                if 'involved_companies' in game:
                    for company_data in game['involved_companies']:
                        if (company_data.get('developer') and 
                            'company' in company_data):
                            company = company_data['company']
                            
                            # Skip if we already have this developer
                            dev_name = company.get('name', '').strip()
                            if not dev_name or dev_name in developers_dict:
                                continue
                            
                            # Extract website URL
                            website_url = ''
                            if 'websites' in company:
                                for website in company['websites']:
                                    # Category 1 is official website
                                    if website.get('category') == 1:
                                        website_url = website.get('url', '')
                                        break
                                # If no official site, take the first one
                                if not website_url and company['websites']:
                                    first_site = company['websites'][0]
                                    website_url = first_site.get('url', '')
                            
                            # Convert start_date timestamp to year
                            founded_year = None
                            if company.get('start_date'):
                                try:
                                    import datetime
                                    timestamp = company['start_date']
                                    date_obj = datetime.datetime.fromtimestamp(timestamp)
                                    founded_year = date_obj.year
                                except (ValueError, TypeError):
                                    founded_year = None
                            
                            developers_dict[dev_name] = {
                                'name': dev_name,
                                'description': company.get('description', ''),
                                'website': website_url,
                                'founded_year': founded_year,
                                'igdb_id': company.get('id')
                            }
                            
                            self.stdout.write(f'Found developer: {dev_name}')
            
            return list(developers_dict.values())
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching from IGDB: {str(e)}')
            )
            return []

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
