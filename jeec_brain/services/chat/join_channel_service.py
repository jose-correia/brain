from config import Config
import requests
import json

import logging

logger = logging.getLogger(__name__)

class JoinChannelService:
    def __init__(self, user, channel_id, channel_code):
        self.channel_id = channel_id
        self.channel_code = channel_code
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/login"
        payload = {"user": user.username, "password": user.password}

        try:
            user = requests.post(url, json=payload)
        except:
            self.auth_token = None
            self.user_id = None

        if not user or not user.json()["status"] == "success":
            self.auth_token = None
            self.user_id = None
        else:
            self.auth_token = user.json()["data"]["authToken"]
            self.user_id = user.json()["data"]["userId"]

    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/channels.join"
        headers = {"X-Auth-Token": self.auth_token, "X-User-Id": self.user_id}
        payload = {"roomId": self.channel_id, "joinCode": self.channel_code}

        try:
            channel = requests.post(url, json=payload, headers=headers)
        except Exception as e:
            logger.exception(e)
            return False

        if not channel or not channel.json()["success"]:
            return False

        return True
