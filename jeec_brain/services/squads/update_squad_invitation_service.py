from typing import Dict, Optional
from jeec_brain.models.squad_invitations import SquadInvitations


class UpdateSquadInvitationService:
    def __init__(self, squad_invitation: SquadInvitations, kwargs: Dict):
        self.squad_invitation = squad_invitation
        self.kwargs = kwargs

    def call(self) -> Optional[SquadInvitations]:
        update_result = self.squad_invitation.update(**self.kwargs)
        return update_result
