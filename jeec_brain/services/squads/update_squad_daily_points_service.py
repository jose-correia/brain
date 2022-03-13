from typing import Dict, Optional
from jeec_brain.models.squads_daily_points import SquadDailyPoints


class UpdateSquadReferralService:
    def __init__(self, squad_daily_points: SquadDailyPoints, kwargs: Dict):
        self.squad_daily_points = squad_daily_points
        self.kwargs = kwargs

    def call(self) -> Optional[SquadDailyPoints]:
        update_result = self.squad_daily_points.update(**self.kwargs)
        return update_result
