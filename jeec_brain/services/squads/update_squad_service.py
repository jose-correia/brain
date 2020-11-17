from typing import Dict, Optional
from jeec_brain.models.squads import Squads


class UpdateSquadService():
    
    def __init__(self, squad: Squads, kwargs: Dict):
        self.squad = squad
        self.kwargs = kwargs

    def call(self) -> Optional[Squads]:
        update_result = self.squad.update(**self.kwargs)
        return update_result
