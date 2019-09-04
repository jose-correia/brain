import logging
from jeec_brain.models.teams import Teams
from jeec_brain.models.colaborators import Colaborators
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateTeamMemberService():

    def __init__(self, team: Teams, payload: Dict):
        self.team = team
        self.name = payload.get('name')
        self.ist_id = payload.get('ist_id')
        self.linkedin_url = payload.get('linkedin_url')
        self.email = payload.get('email')

    def call(self) -> Optional[Colaborators]:
        
        colaborator = Colaborators.create(
            name=self.name,
            ist_id=self.ist_id,
            linkedin_url=self.linkedin_url,
            email=self.email,
            team_id=self.team.id
        )

        if not colaborator:
            return None

        try:
            # add new member to the team
            self.team.members.append(colaborator)
            self.team.save()
        except Exception:
            logger.exception('Failed to add new member to team')
            return None
        
        return colaborator
