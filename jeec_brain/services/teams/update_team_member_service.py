from typing import Dict, Optional
from jeec_brain.models.colaborators import Colaborators


class UpdateTeamMemberService():
    
    def __init__(self, member: Colaborators, kwargs: Dict):
        self.member = member
        self.kwargs = kwargs

    def call(self) -> Optional[Colaborators]:
        update_result = self.member.update(**self.kwargs)
        return update_result
