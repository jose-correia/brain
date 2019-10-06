# SERVICES
from flask import current_app
from jeec_brain.services.event.create_event_service import CreateEventService
from jeec_brain.services.event.update_event_service import UpdateEventService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService


class EventHandler():

    @classmethod
    def create_event(cls, **kwargs):
        return CreateSpeakerService(kwargs=kwargs).call()

    @classmethod
    def update_event(cls, event, **kwargs):
        return UpdateSpeakerService(speaker=speaker, kwargs=kwargs).call()

    @staticmethod
    def upload_image(file, speaker_name):
        return UploadImageService(file, speaker_name, 'static/speakers').call()

    @staticmethod
    def find_image(speaker_name):
        return FindImageService(speaker_name, 'static/speakers').call()

    @staticmethod
    def upload_company_logo(file, company_name):
        return UploadImageService(file, company_name, 'static/speakers/companies').call()

    @staticmethod
    def find_company_logo(company_name):
        return FindImageService(company_name, 'static/speakers/companies').call()
