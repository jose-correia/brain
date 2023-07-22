import logging
from jeec_brain.models.speakers import Speakers
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSpeakerService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Speakers]:

        speaker = Speakers.create(**self.kwargs)

        if not speaker:
            return None

        return speaker
