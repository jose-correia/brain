# SERVICES
from flask import current_app
from jeec_brain.services.squads.create_squad_service import CreateSquadService
from jeec_brain.services.squads.update_squad_service import UpdateSquadService
from jeec_brain.services.squads.delete_squad_service import DeleteSquadService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from jeec_brain.services.squads.create_squad_invitation_service import CreateSquadInvitationService
from jeec_brain.services.squads.delete_squad_invitation_service import DeleteSquadInvitationService
from jeec_brain.services.squads.update_squad_invitation_service import UpdateSquadInvitationService

class SquadsHandler():

    @classmethod
    def create_squad(cls, **kwargs):
        return CreateSquadService(kwargs=kwargs).call()

    @classmethod
    def update_squad(cls, squad, **kwargs):
        return UpdateSquadService(squad=squad, kwargs=kwargs).call()

    @classmethod
    def delete_squad(cls, squad):
        for extension in current_app.config['ALLOWED_IMAGES']:
            image_filename = squad.name.lower().replace(' ', '_') + '.' + extension
            DeleteImageService(image_filename, 'static/squads').call()

        return DeleteSquadService(squad=squad).call()

    @staticmethod
    def upload_squad_image(file, squad_name):
        return UploadImageService(file, squad_name, 'static/squads').call()

    @staticmethod
    def find_squad_image(squad_name):
        return FindImageService(squad_name, 'static/squads').call()

    @classmethod
    def create_squad_invitation(cls, **kwargs):
        return CreateSquadInvitationService(kwargs=kwargs).call()

    @classmethod
    def update_squad_invitation(cls, squad_invitation, **kwargs):
        return UpdateSquadInvitationService(squad_invitation=squad_invitation, kwargs=kwargs).call()

    @classmethod
    def delete_squad_invitation(cls, squad_invitation):
        return DeleteSquadInvitationService(squad_invitation=squad_invitation).call()