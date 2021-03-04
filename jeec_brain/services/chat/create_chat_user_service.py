from jeec_brain.services.chat.update_chat_user_service import UpdateChatUserService
from config import Config
from typing import Dict
import requests
import json
import logging
logger = logging.getLogger(__name__)

class CreateChatUserService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs
        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/login'
        payload = {"user":Config.ROCKET_CHAT_ADMIN_USERNAME, "password":Config.ROCKET_CHAT_ADMIN_PASSWORD}

        try:
            admin = requests.post(url, data=json.dumps(payload))
        except:
            self.auth_token = None
            self.user_id = None

        if not admin or not admin.json()['status'] == 'success':
            self.auth_token = None
            self.user_id = None
        else:
            self.auth_token = admin.json()['data']['authToken']
            self.user_id = admin.json()['data']['userId']


    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/users.create'
        headers={"X-Auth-Token":self.auth_token, "X-User-Id":self.user_id}
        payload={"active":True, "joinDefaultChannels":True, "requirePasswordChange":False, "sendWelcomeEmail":False, "verified":True}
        
        try:
            user = requests.post(url, data=json.dumps({**self.kwargs, **payload}), headers=headers)
        except Exception as e:
            logger.warning(e)
            return None

        if user is None:
            return None
        elif not user.json()['success'] and (self.kwargs.get("username","") + ' is already in use') in user.json()['error']:
            data = self.kwargs
            return UpdateChatUserService(data.pop("username"), data).call()
        elif not user.json()['success']:
            return None

        return user.json()['user']['_id']
