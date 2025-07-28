from igdb.wrapper import IGDBWrapper
import json
import requests
from django.conf import settings
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

    def search_games(self, query, limit=10, offset=0, platform=None):
        """Search for games by name"""
        wrapper = self.initialize_wrapper()

        # Build the query string
        query_parts = [
            f'fields id, name, summary, release_dates.date, platforms.name, cover.url',
            f'search "{query}"',
            f'limit {limit}',
            f'offset {offset}'
        ]

        if platform:
            query_parts.append(f'where platforms = {platform}')

        query_string = '; '.join(query_parts) + ';'

        try:
            byte_array = wrapper.api_request('games', query_string)
            return json.loads(byte_array)
        except Exception as e:
            print(f"Error searching games: {e}")
            return []

    def get_game_by_id(self, game_id):
        """Get a specific game by ID"""
        wrapper = self.initialize_wrapper()

        query_string = f'fields id, name, summary, storyline, release_dates.date, platforms.name, cover.url, screenshots.url, genres.name, involved_companies.company.name, involved_companies.developer, involved_companies.publisher; where id = {game_id};'

        try:
            byte_array = wrapper.api_request('games', query_string)
            games = json.loads(byte_array)
            return games[0] if games else None
        except Exception as e:
            print(f"Error getting game by ID: {e}")
            return None

    def get_games_by_platform(self, platform_id, limit=50, offset=0):
        """Get games by platform ID"""
        wrapper = self.initialize_wrapper()

        query_string = f'fields id, name, summary, release_dates.date, cover.url; where platforms = {platform_id}; limit {limit}; offset {offset};'

        try:
            byte_array = wrapper.api_request('games', query_string)
            return json.loads(byte_array)
        except Exception as e:
            print(f"Error getting games by platform: {e}")
            return []

    def get_platforms(self):
        """Get list of gaming platforms"""
        wrapper = self.initialize_wrapper()

        query_string = 'fields id, name, abbreviation; sort id asc; limit 200;'

        try:
            byte_array = wrapper.api_request('platforms', query_string)
            return json.loads(byte_array)
        except Exception as e:
            print(f"Error getting platforms: {e}")
            return []

    def search_games_with_platforms(self, game_name, limit=10):
        """Search for games by name and return with detailed platform information"""
        wrapper = self.initialize_wrapper()

        query_string = f'fields id, name, summary, release_dates.date, platforms.id, platforms.name, platforms.abbreviation, cover.url; search "{game_name}"; limit {limit};'

        try:
            byte_array = wrapper.api_request('games', query_string)
            games = json.loads(byte_array)

            # Format the results to make platforms easier to work with
            formatted_games = []
            for game in games:
                formatted_game = {
                    'id': game.get('id'),
                    'name': game.get('name'),
                    'summary': game.get('summary', ''),
                    'cover_url': game.get('cover', {}).get('url', '') if game.get('cover') else '',
                    'platforms': []
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

                # Extract release dates
                if 'release_dates' in game:
                    formatted_game['release_dates'] = game['release_dates']

                formatted_games.append(formatted_game)

            return formatted_games
        except Exception as e:
            print(f"Error searching games with platforms: {e}")
            return []

    def get_game_platforms_by_name(self, game_name):
        """Get all platforms for a specific game by name (returns first match)"""
        games = self.search_games_with_platforms(game_name, limit=1)
        if games:
            return {
                'game': games[0],
                'platforms': games[0]['platforms']
            }
        return None


# Convenience function for quick testing
def test_igdb_connection():
    """Test function to verify IGDB connection"""
    try:
        service = IGDBService()
        # Test with a simple search
        games = service.search_games("Mario", limit=5)
        print(f"IGDB Connection Test: Found {len(games)} games")
        for game in games[:3]:
            print(f"- {game.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"IGDB Connection Test Failed: {e}")
        return False


if __name__ == "__main__":
    # For testing purposes
    test_igdb_connection()
