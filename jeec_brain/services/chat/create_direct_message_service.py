from config import Config
import requests
import json

class CreateDirectMessageService():

    def __init__(self, user_sender, user_receiver):
        self.receiver_username = user_receiver.username
        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/login'
        payload = {"user":user_sender.username, "password":user_sender.password}

        try:
            user = requests.post(url, data=json.dumps(payload))
        except:
            self.auth_token = None
            self.user_id = None

        if not user or not user.json()['status'] == 'success':
            self.auth_token = None
            self.user_id = None
        else:
            self.auth_token = user.json()['data']['authToken']
            self.user_id = user.json()['data']['userId']


    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + 'api/v1/im.create'
        headers = {"X-Auth-Token":self.auth_token, "X-User-Id":self.user_id}
        payload = {"username":self.receiver_username}
        
        try:
            room = requests.post(url, data=json.dumps(payload), headers=headers)
        except:
            return None

        if not room or not room.json()['success']:
            return None

        return room.json()['room']['rid']