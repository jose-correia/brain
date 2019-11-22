import logging
from jeec_brain.models.users import Users
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateUserService():

    def __init__(self, company_id, username, email, role):
        self.company_id = company_id
        self.username = username
        self.email = email
        self.role = role

    def call(self) -> Optional[Users]:
        
        user = Users.create(
            company_id=self.company_id,
            username=self.username,
            email=self.email,
            role=self.role
        )

        if not user:
            return None

        return user

