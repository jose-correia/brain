import logging
from jeec_brain.models.squads_daily_points import SquadDailyPoints
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSquadDailyPointsService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[SquadDailyPoints]:
        
        squad_daily_points = SquadDailyPoints.create(**self.kwargs)

        if not squad_daily_points:
            return None

        return squad_daily_points
