# SERVICES
from flask import current_app
from jeec_brain.services.speakers.create_speaker_service import CreateSpeakerService
from jeec_brain.services.speakers.update_speaker_service import UpdateSpeakerService
from jeec_brain.services.speakers.delete_speaker_service import DeleteSpeakerService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService


class SpeakersHandler:
    @classmethod
    def create_speaker(cls, **kwargs):
        return CreateSpeakerService(kwargs=kwargs).call()

    @classmethod
    def update_speaker(cls, speaker, **kwargs):
        return UpdateSpeakerService(speaker=speaker, kwargs=kwargs).call()

    @classmethod
    def delete_speaker(cls, speaker):
        speaker_name = speaker.name
        speaker_company_name = speaker.company

        if DeleteSpeakerService(speaker=speaker).call():
            for extension in current_app.config["ALLOWED_IMAGES"]:
                image_filename = (
                    speaker_name.lower().replace(" ", "_") + "." + extension
                )
                company_logo_filename = (
                    speaker_company_name.lower().replace(" ", "_") + "." + extension
                )

                DeleteImageService(image_filename, "static/speakers").call()
                DeleteImageService(
                    company_logo_filename, "static/speakers/companies"
                ).call()
            return True
        return False

    @staticmethod
    def upload_image(file, speaker_name):
        return UploadImageService(file, speaker_name, "static/speakers").call()

    @staticmethod
    def find_image(speaker_name):
        return FindImageService(speaker_name, "static/speakers").call()

    @staticmethod
    def upload_company_logo(file, company_name):
        return UploadImageService(
            file, company_name, "static/speakers/companies"
        ).call()

    @staticmethod
    def find_company_logo(company_name):
        return FindImageService(company_name, "static/speakers/companies").call()
