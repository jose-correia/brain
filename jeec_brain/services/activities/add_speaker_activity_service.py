from typing import Optional
from jeec_brain.models.speaker_activities import SpeakerActivities


class AddSpeakerActivityService():
    def __init__(self, speaker_id: int, activity_id: int):
        self.speaker_id = speaker_id
        self.activity_id = activity_id

    def call(self) -> Optional[SpeakerActivities]:
        speaker_activity = SpeakerActivities.create(
            speaker_id=self.speaker_id,
            activity_id=self.activity_id
        )
        return speaker_activity
