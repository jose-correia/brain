# SERVICES
import os
from flask import current_app
from jeec_brain.services.teams.create_team_service import CreateTeamService
from jeec_brain.services.teams.update_team_service import UpdateTeamService
from jeec_brain.services.teams.delete_team_service import DeleteTeamService
from jeec_brain.services.teams.delete_team_member_service import DeleteTeamMemberService
from jeec_brain.services.teams.update_team_member_service import UpdateTeamMemberService
from jeec_brain.services.teams.create_team_member_service import CreateTeamMemberService

import logging
logger = logging.getLogger(__name__)


def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGES']


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

    @staticmethod
    def upload_member_image(file, member_name):
        if file.filename == '':
            return False, 'No file selected for uploading'

        if file and allowed_image(file.filename):
            filename = member_name.lower().replace(' ', '_') + '.png'
            try:
                file.save(os.path.join(current_app.root_path, 'static', 'members', filename))
                return True, None
            
            except Exception as e:
                logger.error(e)
                return False, 'Image upload failed'

        return False, 'File extension is not allowed'

    @staticmethod
    def delete_member_image(member_name):
        filename = member_name.lower().replace(' ', '_') + '.png'

        try:
            os.remove(os.path.join(current_app.root_path, 'static', 'members', filename))
            return True
        except Exception as e:
            return False

    @staticmethod
    def find_member_image(member_name):
        image_filename = member_name.lower().replace(' ', '_') + '.png'

        if not os.path.isfile(os.path.join(current_app.root_path, 'static', 'members', image_filename)): 
            return None
        else:
            return f'/static/members/{image_filename}'
