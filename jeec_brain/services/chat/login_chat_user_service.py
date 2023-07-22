from config import Config
import requests
import json

import logging

logger = logging.getLogger(__name__)

class LoginChatUserService:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/login"
        payload = {"user": self.username, "password": self.password}

        try:
            user = requests.post(url, json=payload)
        except Exception as e:
            logger.error(e)
            return None

        if not user or not user.json()["status"] == "success":
            return None
        else:
            return user.json()["data"]
