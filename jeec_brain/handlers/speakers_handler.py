# SERVICES
import os
from flask import current_app
from jeec_brain.services.speakers.create_speaker_service import CreateSpeakerService
from jeec_brain.services.speakers.update_speaker_service import UpdateSpeakerService
from jeec_brain.services.speakers.delete_speaker_service import DeleteSpeakerService

import logging
logger = logging.getLogger(__name__)


def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGES']


class SpeakersHandler():

    @classmethod
    def create_speaker(cls, **kwargs):
        return CreateSpeakerService(payload=kwargs).call()

    @classmethod
    def update_speaker(cls, speaker, **kwargs):
        return UpdateSpeakerService(speaker=speaker, kwargs=kwargs).call()

    @classmethod
    def delete_speaker(cls, speaker):
        return DeleteSpeakerService(speaker=speaker).call()

    @staticmethod
    def upload_image(file, speaker_name):
        if file.filename == '':
            return False, 'No file selected for uploading'

        if file and allowed_image(file.filename):
            filename = speaker_name.lower().replace(' ', '_') + '.png'
            try:
                file.save(os.path.join(current_app.root_path, 'static', 'speakers', filename))
                return True, None
            
            except Exception as e:
                logger.error(e)
                return False, e

        return False, 'File extension is not allowed'

    @staticmethod
    def delete_image(speaker_name):
        filename = speaker_name.lower().replace(' ', '_') + '.png'

        try:
            os.remove(os.path.join(current_app.root_path, 'static', 'speakers', filename))
            return True
        except Exception as e:
            return False

    @staticmethod
    def find_image(speaker_name):
        image_filename = speaker_name.lower().replace(' ', '_') + '.png'
        image_path = f'/static/speakers/{image_filename}'

        if not os.path.isfile(os.path.join(current_app.root_path, 'static', 'speakers', image_filename)): 
            image_path = None
        else:
            return image_path

    