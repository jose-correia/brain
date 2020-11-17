import logging
from jeec_brain.models.squads import Squads
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSquadService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Squads]:
        
        squad = Squads.create(**self.kwargs)

        if not squad:
            return None

        return squad
