from config import Config
import requests
import json


class LoginChatUserService:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def call(self):
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/login"
        payload = {"user": self.username, "password": self.password}

        try:
            user = requests.post(url, data=json.dumps(payload))
        except:
            return None

        if not user or not user.json()["status"] == "success":
            return None
        else:
            return user.json()["data"]
