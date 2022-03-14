from config import Config
import requests
import json


class DeleteChatUserService:
    def __init__(self, user):
        self.user = user
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
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/users.delete"
        headers = {"X-Auth-Token": self.auth_token, "X-User-Id": self.user_id}
        payload = {"username": self.user.username}

        try:
            result = requests.post(url, json=payload, headers=headers)
        except:
            return False

        if not result or not result.json()["success"]:
            return False

        return True
