from datetime import datetime, timezone, timedelta
import base64
import requests
import logging

logger = logging.getLogger(__name__)


class AuthManager:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self._auth_url = base_url + '/token'
        self._token = None
        self._expires_at = None

    def get_token(self):
        """Get OAuth token from DICE API"""

        # Return cached token if valid
        if self._token and self._expires_at and self._expires_at > datetime.now(timezone.utc):
            return self._token

        # Otherwise fetch new token
        result = self._fetch_new_token()
        if result is None:
            logger.error('Token Fetching Failed!!!')
            return None

        return result

    def _fetch_new_token(self):
        """Generate new token from DICE API"""
        try:
            credentials = f"{self.username}:{self.password}"
            auth_header = base64.b64encode(credentials.encode()).decode()

            headers = {
                'Authorization': f'Basic {auth_header}',
                'User-Agent': 'Python Requests'
            }

            response = requests.get(self._auth_url, headers=headers, timeout=10)

            if not response.ok:
                logger.error(f'DICE Token generation Failed with error: {response.text}')
                return None
            
            # access_token:{
            #     data:{
            #         access_token: {...}
            #     }
            # }
            result = response.json()
            access_token_obj = result.get('access_token')
            data = access_token_obj.get('data') if access_token_obj else None
            token = data.get('access_token') if data else None

            if token:
                self._token = token
                self._expires_at = datetime.now(timezone.utc) + timedelta(days=6)
                logger.info('DICE API token generated successfully')
            else:
                logger.error('Token not found in response')

            return token

        except Exception as e:
            logger.error(f'Error getting DICE token: {e}')
            return None