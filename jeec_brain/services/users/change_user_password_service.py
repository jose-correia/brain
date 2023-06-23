import logging
from jeec_brain.models.users import Users
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ChangeUserPasswordService:
    def __init__(self, user: Users):
        self.user = user

    def call(self, new_password) -> bool:

        user = Users.update(
            self.user,
            name=self.user.name,
            username=self.user.username,
            email=self.user.email,
            role=self.user.role,
            password=new_password,
            chat_id=self.user.chat_id,
        )

        if not user:
            return None

        return user