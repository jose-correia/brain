from config import Config
from typing import Dict
import requests
import json

class UpdateChatUserService():

    def __init__(self, username, kwargs: Dict):
        self.username = username
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
        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/users.info'
        headers={"X-Auth-Token":self.auth_token, "X-User-Id":self.user_id}
        
        try:
            user = requests.get(url + '?username=' + self.username, headers=headers)
        except:
            return None

        if not user or not user.json()['success']:
            return None

        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/users.update'

        try:
            user = requests.post(url, data=json.dumps({'userId':user.json()['user']['_id'], 'data':self.kwargs}), headers=headers)
        except:
            return None

        if not user or not user.json()['success']:
            return None
       
        return user.json()['user']['_id']
