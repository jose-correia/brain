import logging
from jeec_brain.models.teams import Teams
from jeec_brain.models.colaborators import Colaborators
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateTeamMemberService:
    def __init__(self, team: Teams, kwargs: Dict):
        self.team = team
        self.kwargs = kwargs

    def call(self) -> Optional[Colaborators]:

        colaborator = Colaborators.create(team_id=self.team.id, **self.kwargs)

        if not colaborator:
            return None

        try:
            # add new member to the team
            self.team.members.append(colaborator)
            self.team.save()
        except Exception:
            logger.exception("Failed to add new member to team")
            return None

        return colaborator
