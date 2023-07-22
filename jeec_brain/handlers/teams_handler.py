# SERVICES
from flask import current_app
from jeec_brain.services.teams.create_team_service import CreateTeamService
from jeec_brain.services.teams.update_team_service import UpdateTeamService
from jeec_brain.services.teams.delete_team_service import DeleteTeamService
from jeec_brain.services.teams.delete_team_member_service import DeleteTeamMemberService
from jeec_brain.services.teams.update_team_member_service import UpdateTeamMemberService
from jeec_brain.services.teams.create_team_member_service import CreateTeamMemberService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from jeec_brain.services.files.get_file_service import GetFileImage


class TeamsHandler:
    @classmethod
    def create_team(cls, **kwargs):
        return CreateTeamService(kwargs=kwargs).call()

    @classmethod
    def update_team(cls, team, **kwargs):
        return UpdateTeamService(team=team, kwargs=kwargs).call()

    @classmethod
    def delete_team(cls, team):
        # first we delete all the member's images
        for member in team.members:
            for extension in current_app.config["ALLOWED_IMAGES"]:
                image_filename = member.name.lower().replace(" ", "_") + "." + extension
                DeleteImageService(image_filename, "static/members").call()

        # finally delete team
        return DeleteTeamService(team=team).call()

    @classmethod
    def create_team_member(cls, team, **kwargs):
        return CreateTeamMemberService(team=team, kwargs=kwargs).call()

    @classmethod
    def update_team_member(cls, member, **kwargs):
        return UpdateTeamMemberService(member=member, kwargs=kwargs).call()

    @classmethod
    def delete_team_member(cls, member):
        member_name = member.name

        if DeleteTeamMemberService(member=member).call():
            for extension in current_app.config["ALLOWED_IMAGES"]:
                filename = member_name.lower().replace(" ", "_") + "." + extension
                DeleteImageService(filename, "static/members").call()
            return True
        return False

    @staticmethod
    def upload_member_image(file, member_name):
        return UploadImageService(file, member_name, "static/members").call()

    @staticmethod
    def get_image_member(member_name):
        return GetFileImage(member_name, "static/members").call()

    @staticmethod
    def find_member_image(member_name):
        return FindImageService(member_name, "static/members").call()
