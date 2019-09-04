# SERVICES
from jeec_brain.services.teams.create_team_service import CreateTeamService
from jeec_brain.services.teams.update_team_service import UpdateTeamService
from jeec_brain.services.teams.delete_team_service import DeleteTeamService
from jeec_brain.services.teams.delete_team_member_service import DeleteTeamMemberService
from jeec_brain.services.teams.update_team_member_service import UpdateTeamMemberService
from jeec_brain.services.teams.create_team_member_service import CreateTeamMemberService


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

    @classmethod
    def create_team_member(cls, team, **kwargs):
        return CreateTeamMemberService(team=team, payload=kwargs).call()

    @classmethod
    def update_team_member(cls, member, **kwargs):
        return UpdateTeamMemberService(member=member, kwargs=kwargs).call()

    @classmethod
    def delete_team_member(cls, member):
        return DeleteTeamMemberService(member=member).call()
