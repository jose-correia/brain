import logging
from jeec_brain.models.teams import Teams
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateTeamService():

    def __init__(self, payload: Dict):
        self.name = payload.get('name')
        self.description = payload.get('description')

    def call(self) -> Optional[Teams]:
        
        team = Teams.create(
            name=self.name,
            description=self.description
        )

        if not team:
            return None

        return team
