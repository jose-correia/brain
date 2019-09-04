# SERVICES
from jeec_brain.services.teams.create_team_service import CreateTeamService
from jeec_brain.services.teams.update_team_service import UpdateTeamService
from jeec_brain.services.teams.delete_team_service import DeleteTeamService


class TeamsHandler():

    @classmethod
    def create_team(cls, **kwargs):
        return CreateTeamService(payload=kwargs).call()

    @classmethod
    def update_team(cls, team, **kwargs):
        return UpdateTeamService(team=team, kwargs=kwargs).call()

    @classmethod
    def delete_team(cls, team):
        return DeleteTeamService(team=team).call()
