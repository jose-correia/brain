from typing import Dict, Optional
from jeec_brain.models.speakers import Speakers


class UpdateSpeakerService():
    
    def __init__(self, speaker: Speakers, kwargs: Dict):
        self.speaker = speaker
        self.kwargs = kwargs

    def call(self) -> Optional[Speaker]:
        update_result = self.speaker.update(**self.kwargs)
        return update_result
