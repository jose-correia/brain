# SERVICES
from jeec_brain.services.speakers.create_speaker_service import CreateSpeakerService
from jeec_brain.services.speakers.update_speaker_service import UpdateSpeakerService
from jeec_brain.services.speakers.delete_speaker_service import DeleteSpeakerService


class SpeakersHandler():

    @classmethod
    def create_speaker(cls, **kwargs):
        return CreateSpeakerService(kwargs=kwargs).call()

    @classmethod
    def update_speaker(cls, speaker, **kwargs):
        return UpdateSpeakerService(speaker=speaker, kwargs=kwargs).call()

    @classmethod
    def delete_speaker(cls, speaker):
        return DeleteSpeakerService(speaker=speaker).call()
