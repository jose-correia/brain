from typing import Dict, Optional
from jeec_brain.models.speaker_activities import SpeakerActivities


class UpdateSpeakerActivityService():
    
    def __init__(self, speaker_activity: SpeakerActivities, speaker_id: int, activity_id: int):
        self.speaker_activity = speaker_activity
        self.speaker_id = speaker_id
        self.activity_id = activity_id

    def call(self) -> Optional[SpeakerActivities]:
        update_result = self.speaker_activity.update(
            speaker_id=self.speaker_id,
            activity_id=self.activity_id
        )
        return update_result
