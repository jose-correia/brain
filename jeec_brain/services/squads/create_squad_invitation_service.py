import logging
from jeec_brain.models.squad_invitations import SquadInvitations
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSquadInvitationService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[SquadInvitations]:
        
        squad_invitation = SquadInvitations.create(**self.kwargs)

        if not squad_invitation:
            return None

        return squad_invitation
