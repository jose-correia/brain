import logging
from jeec_brain.models.teams import Teams
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateTeamService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Teams]:
        
        team = Teams.create(**self.kwargs)

        if not team:
            return None

        return team
