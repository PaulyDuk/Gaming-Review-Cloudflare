from django.core.management.base import BaseCommand
from reviews.igdb_service import IGDBService
import json


class Command(BaseCommand):
    help = 'Test IGDB API connection and print all fields for Doom Eternal'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing IGDB API for Doom Eternal...'))
        service = IGDBService()
        wrapper = service.initialize_wrapper()
        query_string = 'search "Doom Eternal"; limit 1; fields involved_companies.developer, involved_companies.publisher;'
        try:
            byte_array = wrapper.api_request('games', query_string)
            games = json.loads(byte_array)
            if games:
                game = games[0]
                if 'involved_companies' in game:
                    developers = []
                    publishers = []
                    for company in game['involved_companies']:
                        if company.get('developer'):
                            developers.append(company)
                        if company.get('publisher'):
                            publishers.append(company)
                    self.stdout.write(self.style.SUCCESS("Developers:"))
                    for dev in developers:
                        self.stdout.write(str(dev))
                    self.stdout.write(self.style.SUCCESS("Publishers:"))
                    for pub in publishers:
                        self.stdout.write(str(pub))
                else:
                    self.stdout.write(self.style.WARNING("No involved_companies found for 'Doom Eternal'"))
            else:
                self.stdout.write(self.style.WARNING("No results found for 'Doom Eternal'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
