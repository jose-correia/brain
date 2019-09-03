from typing import Dict, Optional
from jeec_brain.models.teams import Teams


class UpdateTeamService():
    
    def __init__(self, team: team, kwargs: Dict):
        self.team = team
        self.kwargs = kwargs

    def call(self) -> Optional[Teams]:
        update_result = self.team.update(**self.kwargs)
        return update_result
