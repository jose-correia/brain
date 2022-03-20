from config import Config
import requests
import json

import logging

logger = logging.getLogger(__name__)

class GetChannelInfoService:
    def __init__(self, name):
        self.name = name
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/login"
        payload = {
            "user": Config.ROCKET_CHAT_ADMIN_USERNAME,
            "password": Config.ROCKET_CHAT_ADMIN_PASSWORD,
        }

        try:
            admin = requests.post(url, json=payload)
        except:
            self.auth_token = None
            self.user_id = None

        if not admin or not admin.json()["status"] == "success":
            self.auth_token = None
            self.user_id = None
        else:
            self.auth_token = admin.json()["data"]["authToken"]
            self.user_id = admin.json()["data"]["userId"]

    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/channels.info?roomName=" + self.name
        headers = {"X-Auth-Token": self.auth_token, "X-User-Id": self.user_id}

        try:
            channel = requests.post(url, headers=headers)
        except Exception as e:
            logger.error(e)
            return None

        if not channel or not channel.json()["success"]:
            return None

        return channel.json()["channel"]
