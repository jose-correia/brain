import logging
from jeec_brain.models.activities import Activities
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateActivityService():

    def __init__(self, payload: Dict):
        self.name = payload.get('name')
        self.description = payload.get('description')
        self.location = payload.get('location')
        self.day = payload.get('day')
        self.time = payload.get('time')
        self.type = payload.get('type')
        self.registration_open = payload.get('registration_open')
        self.registration_link = payload.get('registration_link')

    def call(self) -> Optional[Activities]:
        
        activity = Activities.create(
            name=self.name,
            description=self.description,
            location=self.location,
            day=self.day,
            time=self.time,
            type=self.type,
            registration_open=self.registration_open,
            registration_link=self.registration_link,
        )

        if not activity:
            return None

        return activity

