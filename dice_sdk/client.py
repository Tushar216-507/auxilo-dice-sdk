import logging
from .auth import AuthManager
from .base_client import BaseClient
from .channels.email import EmailClient
from .channels.whatsapp import WhatsappClient
from .channels.sms import SmsClient

logger = logging.getLogger(__name__)

class DiceClient:
    def __init__(self,username,password,base_url):
        self._auth = AuthManager(username,password,base_url)
        self._base_client = BaseClient(self._auth,base_url)
        self.email = EmailClient(self._base_client)
        self.whatsapp = WhatsappClient(self._base_client)
        self.sms = SmsClient(self._base_client)