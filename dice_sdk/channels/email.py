import logging
from ..base_client import BaseClient

logger = logging.getLogger(__name__)

class EmailClient:
    def __init__(self,base_client):
        self.client = base_client

    def send(self, email, template_id, template_attr,subject,email_from_name,source='SDK',message_type = 'transactional'):
        payload = {
            'email': email,
            'channel': 'email',
            'source': source,
            'type': message_type,
            'template_id': template_id,
            'email_subject': subject,
            'email_from_name': email_from_name,
            'template_attr': template_attr
        }
        
        return self.client._post(payload)
            
        