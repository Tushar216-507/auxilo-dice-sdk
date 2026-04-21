import logging
from ..base_client import BaseClient

logger = logging.getLogger(__name__)

class SmsClient:
    def __init__(self,base_client):
        self.client = base_client

    def send(self,template_id,template_attr,mobile_no: str,source = 'SDK',message_type = 'transactional'):
        if not mobile_no or mobile_no.strip() == '':
            return {
                'success': False,
                'message': 'SMS Notification are disabled'
            }
        
        clean_mobile = ''.join(filter(str.isdigit,str(mobile_no)))
        if not clean_mobile:
            return {
                'success': False,
                'message': 'Invalid mobile number'
            }
        
        if len(clean_mobile) == 10:
            formatted_mobile = f'91{clean_mobile}'
        elif len(clean_mobile) == 12 and clean_mobile.startswith('91'):
            formatted_mobile = f'{clean_mobile}'
        else:
            formatted_mobile = f'+91{clean_mobile[-10:]}'

        payload = {
            'mobile_no': formatted_mobile,
            'channel': 'sms',
            'source': source,
            'type': message_type,
            'template_id': template_id,
            'template_attr': template_attr
        }
        return self.client._post(payload)
