import logging
from jeec_brain.models.users import Users
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateUserService():

    def __init__(self, company_id, username, email, role, password, food_manager):
        self.company_id = company_id
        self.username = username
        self.email = email
        self.role = role
        self.password = password
        self.food_manager = food_manager

    def call(self) -> Optional[Users]:
        
        user = Users.create(
            company_id=self.company_id,
            username=self.username,
            email=self.email,
            role=self.role,
            password=self.password,
            food_manager=self.food_manager
        )

        if not user:
            return None

        return user

