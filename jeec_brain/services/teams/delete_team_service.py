from jeec_brain.models.teams import Teams


class DeleteTeamService():

    def __init__(self, team: Teams):
        self.team = team

    def call(self) -> bool:
        result = self.team.delete()
        return result
