from jeec_brain.models.colaborators import Colaborators


class DeleteTeamMemberService():

    def __init__(self, member: Colaborators):
        self.member = member

    def call(self) -> bool:
        result = self.member.delete()
        return result
