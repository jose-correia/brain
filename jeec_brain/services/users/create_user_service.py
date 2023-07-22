import logging
from jeec_brain.models.users import Users
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateUserService:
    def __init__(self, name, username, email, role, password, chat_id):
        self.name = name
        self.username = username
        self.email = email
        self.role = role
        self.password = password
        self.chat_id = chat_id

    def call(self) -> Optional[Users]:

        user = Users.create(
            name=self.name,
            username=self.username,
            email=self.email,
            role=self.role,
            password=self.password,
            chat_id=self.chat_id,
        )

        if not user:
            return None

        return user
