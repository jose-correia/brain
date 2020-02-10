from jeec_brain.models.speaker_activities import SpeakerActivities


class DeleteSpeakerActivityService():

    def __init__(self, speaker_activity: SpeakerActivities):
        self.speaker_activity = speaker_activity

    def call(self) -> bool:
        result = self.speaker_activity.delete()
        return result
