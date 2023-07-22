from jeec_brain.models.speakers import Speakers


class DeleteSpeakerService:
    def __init__(self, speaker: Speakers):
        self.speaker = speaker

    def call(self) -> bool:
        result = self.speaker.delete()
        return result
