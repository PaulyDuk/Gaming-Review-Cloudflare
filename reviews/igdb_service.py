from igdb.wrapper import IGDBWrapper
from django.conf import settings
import json
import requests
import os


class IGDBService:
    """Service class for interacting with IGDB API"""

    def __init__(self):
        self.client_id = getattr(settings, 'IGDB_CLIENT_ID', None) or os.getenv('IGDB_CLIENT_ID')
        self.client_secret = getattr(settings, 'IGDB_CLIENT_SECRET', None) or os.getenv('IGDB_CLIENT_SECRET')
        self.access_token = None
        self.wrapper = None

        if not self.client_id or not self.client_secret:
            raise ValueError("IGDB_CLIENT_ID and IGDB_CLIENT_SECRET must be set in settings or environment variables")

    def get_access_token(self):
        """Get Twitch access token for IGDB API"""
        if self.access_token:
            return self.access_token

        url = "https://id.twitch.tv/oauth2/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return self.access_token
        else:
            raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

    def initialize_wrapper(self):
        """Initialize IGDB wrapper with credentials"""
        if not self.wrapper:
            if not self.access_token:
                self.get_access_token()
            self.wrapper = IGDBWrapper(self.client_id, self.access_token)
        return self.wrapper

    def get_game_platforms_by_name(self, game_name):
        """Get platforms, genres, developers, and publishers for a game by name
        (returns first match)"""
        games = self.search_games_with_platforms(game_name, limit=1)
        if games:
            return {
                'game': games[0],
                'platforms': games[0]['platforms'],
                'genres': games[0]['genres'],
                'developers': games[0]['developers'],
                'publishers': games[0]['publishers']
            }
        return None

    def search_games_with_platforms(self, game_name, limit=10):
        """Search for games by name and return with detailed platform information"""
        wrapper = self.initialize_wrapper()

        query_string = (
            f'fields id, name, summary, release_dates.date, '
            f'release_dates.platform.name, platforms.id, platforms.name, '
            f'platforms.abbreviation, cover.url, genres.name, '
            f'involved_companies.company.name, '
            f'involved_companies.company.description, '
            f'involved_companies.company.websites.url, '
            f'involved_companies.company.websites.category, '
            f'involved_companies.company.start_date, '
            f'involved_companies.company.logo.url, '
            f'involved_companies.developer, involved_companies.publisher; '
            f'search "{game_name}"; limit {limit};'
        )

        try:
            byte_array = wrapper.api_request('games', query_string)
            games = json.loads(byte_array)

            # Format the results to make platforms easier to work with
            formatted_games = []
            for game in games:
                cover_url = (game.get('cover', {}).get('url', '') if game.get('cover') else '')
                if cover_url:
                    cover_url = cover_url.replace('t_thumb', 't_cover_big')
                formatted_game = {
                    'id': game.get('id'),
                    'name': game.get('name'),
                    'summary': game.get('summary', ''),
                    'cover_url': cover_url,
                    'platforms': [],
                    'genres': [],
                    'developers': [],
                    'publishers': []
                }

                # Extract platform information
                if 'platforms' in game:
                    for platform in game['platforms']:
                        platform_info = {
                            'id': platform.get('id'),
                            'name': platform.get('name'),
                            'abbreviation': platform.get('abbreviation', '')
                        }
                        formatted_game['platforms'].append(platform_info)

                # Extract genre information
                if 'genres' in game:
                    for genre in game['genres']:
                        genre_info = {
                            'id': genre.get('id'),
                            'name': genre.get('name')
                        }
                        formatted_game['genres'].append(genre_info)

                # Extract developer information
                if 'involved_companies' in game:
                    for company_data in game['involved_companies']:
                        if (company_data.get('developer') and
                                'company' in company_data):
                            company = company_data['company']

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
                            founded_year = ''
                            if company.get('start_date'):
                                try:
                                    import datetime
                                    timestamp = company['start_date']
                                    if isinstance(timestamp, (int, float)) and timestamp > 0:
                                        date_obj = datetime.datetime.fromtimestamp(timestamp)
                                        founded_year = date_obj.year
                                    else:
                                        founded_year = ''
                                except (ValueError, TypeError, OSError):
                                    founded_year = ''

                            # Extract logo URL
                            logo_url = ''
                            if company.get('logo') and company['logo'].get('url'):
                                logo_url = company['logo']['url']
                                # Convert to HTTPS and larger size
                                if logo_url.startswith('//'):
                                    logo_url = 'https:' + logo_url
                                # Replace t_thumb with t_logo_med for better quality
                                logo_url = logo_url.replace('t_thumb', 't_logo_med')

                            developer_info = {
                                'id': company.get('id'),
                                'name': company.get('name', ''),
                                'description': company.get('description', ''),
                                'website': website_url,
                                'founded_year': founded_year,
                                'logo_url': logo_url
                            }
                            formatted_game['developers'].append(developer_info)

                # Extract publisher information
                if 'involved_companies' in game:
                    for company_data in game['involved_companies']:
                        if (company_data.get('publisher') and
                                'company' in company_data):
                            company = company_data['company']

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
                            founded_year = ''
                            if company.get('start_date'):
                                try:
                                    import datetime
                                    timestamp = company['start_date']
                                    if isinstance(timestamp, (int, float)) and timestamp > 0:
                                        date_obj = datetime.datetime.fromtimestamp(timestamp)
                                        founded_year = date_obj.year
                                    else:
                                        founded_year = ''
                                except (ValueError, TypeError, OSError):
                                    founded_year = ''

                            # Extract logo URL
                            logo_url = ''
                            if company.get('logo') and company['logo'].get('url'):
                                logo_url = company['logo']['url']
                                # Convert to HTTPS and larger size
                                if logo_url.startswith('//'):
                                    logo_url = 'https:' + logo_url
                                # Replace t_thumb with t_logo_med for better quality
                                logo_url = logo_url.replace('t_thumb', 't_logo_med')

                            publisher_info = {
                                'id': company.get('id'),
                                'name': company.get('name', ''),
                                'description': company.get('description', ''),
                                'website': website_url,
                                'founded_year': founded_year,
                                'logo_url': logo_url
                            }
                            formatted_game['publishers'].append(publisher_info)

                # Extract release dates with platform information
                if 'release_dates' in game:
                    formatted_game['release_dates'] = game['release_dates']

                formatted_games.append(formatted_game)

            return formatted_games
        except Exception as e:
            print(f"Error searching games with platforms: {e}")
            import traceback
            traceback.print_exc()
            return []
