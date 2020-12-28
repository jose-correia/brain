from jeec_brain.models.squad_invitations import SquadInvitations


class DeleteSquadInvitationService():

    def __init__(self, squad_invitation: SquadInvitations):
        self.squad_invitation = squad_invitation

    def call(self) -> bool:
        result = self.squad_invitation.delete()
        return result
