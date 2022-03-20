from config import Config
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)
import requests
import json

import logging

logger = logging.getLogger(__name__)


class CreateChannelService:
    def __init__(self, name, members=[]):
        self.name = (
            name.replace(" ", "_")
            .replace("&", " and ")
            .replace("ç", "c")
            .replace(":", " ")
        )
        self.members = members
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
        url = Config.ROCKET_CHAT_APP_URL + "api/v1/channels.create"
        headers = {"X-Auth-Token": self.auth_token, "X-User-Id": self.user_id}
        payload = {"name": self.name, "members": self.members}

        try:
            channel = requests.post(url, json=payload, headers=headers)
        except Exception as e:
            logger.warning(e)
            return None, None

        if not channel or not channel.json()["success"]:
            return None, None

        url = Config.ROCKET_CHAT_APP_URL + "api/v1/channels.setJoinCode"
        joinCode = GenerateCredentialsService().call()
        payload = {"roomId": channel.json()["channel"]["_id"], "joinCode": joinCode}

        try:
            channel = requests.post(url, json=payload, headers=headers)
        except:
            return None, None

        if not channel or not channel.json()["success"]:
            return None, None

        return channel.json()["channel"]["_id"], joinCode
