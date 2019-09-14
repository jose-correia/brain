import logging
from jeec_brain.models.speakers import Speakers
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSpeakerService():

    def __init__(self, payload: Dict):
        self.name = payload.get('name')
        self.company = payload.get('company')
        self.position = payload.get('position')
        self.country = payload.get('country')
        self.bio = payload.get('bio')
        self.linkedin_url = payload.get('linkedin_url')
        self.spotlight = payload.get('spotlight')

    def call(self) -> Optional[Speakers]:
        
        speaker = Speakers.create(
            name=self.name,
            company=self.company,
            position=self.position,
            country=self.country,
            bio=self.bio,
            linkedin_url=self.linkedin_url,
            spotlight=self.spotlight
        )

        if not speaker:
            return None

        return speaker
