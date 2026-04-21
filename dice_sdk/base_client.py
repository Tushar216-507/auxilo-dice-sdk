import logging 
import requests
import sys
import platform
from .exceptions import DiceSendError, DiceConnectionError, DiceNewIPError, DiceTokenExpiredError, DiceAuthError, DiceTemplateError, DiceValidationError

logger = logging.getLogger(__name__)

class BaseClient:
    def __init__(self,auth_manager,base_url):
        self.auth = auth_manager
        self.base_url = base_url
        self._message_url = base_url + '/send-message/v1'

    def _post(self, payload):
        token = self.auth.get_token()
        if not token:
            raise DiceAuthError('Token not found')
        
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Python Requests',
            'Content-Type': 'application/json',
            'X-Dice-SDK-Version': '1.0.0',
            'X-Dice-SDK-Runtime': f'Python {sys.version.split()[0]}',
            'X-Dice-SDK-Platform': platform.system()
        }

        template_id = payload.get('template_id')
        if template_id is None:
            raise DiceValidationError('template_id is required')

        
        try:
            response = requests.post(self._message_url, json=payload, headers=headers, timeout=10)
            logger.info(f'DICE message sent | template = {template_id} | status = {response.status_code}')

            if response.status_code == 401:
                raise DiceTokenExpiredError("Token expired")

            if response.status_code == 403:
                raise DiceNewIPError("Request blocked — new IP detected. Check your email to approve.")

            if response.status_code == 404:
                raise DiceTemplateError(f'Template "{template_id}" not found in DICE')

            try:
                data = response.json()
            except Exception:
                data = response.text

            if response.ok:
                return {
                    'success': True,
                    'response_status': response.status_code,
                    'data': data
                }
            else:
                logger.error(f'DICE API Error: {response.text}')
                return {
                    'success': False,
                    'response_status': response.status_code,
                    'error': data
                }

        except requests.exceptions.ConnectionError:
            raise DiceConnectionError("Could not reach DICE server")
