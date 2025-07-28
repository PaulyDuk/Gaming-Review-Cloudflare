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


    def get_game_platforms_by_name(self, game_name):
        """Get platforms and genres for a game by name (returns first match)"""
        games = self.search_games_with_platforms(game_name, limit=1)
        if games:
            return {
                'game': games[0],
                'platforms': games[0]['platforms'],
                'genres': games[0]['genres']
            }
        return None


    def search_games_with_platforms(self, game_name, limit=10):
        """Search for games by name and return with detailed platform information"""
        wrapper = self.initialize_wrapper()

        query_string = (
            f'fields id, name, summary, release_dates.date, '
            f'release_dates.platform.name, platforms.id, platforms.name, '
            f'platforms.abbreviation, cover.url, genres.name; '
            f'search "{game_name}"; limit {limit};'
        )

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
                    'platforms': [],
                    'genres': []
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

                # Extract release dates with platform information
                if 'release_dates' in game:
                    formatted_game['release_dates'] = game['release_dates']

                formatted_games.append(formatted_game)

            return formatted_games
        except Exception as e:
            print(f"Error searching games with platforms: {e}")
            return []
        

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
