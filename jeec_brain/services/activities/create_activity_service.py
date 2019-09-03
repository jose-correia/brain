import logging
from jeec_brain.models.activities import Activities
from jeec_brain.models.companies import Companies
from jeec_brain.models.speakers import Speakers
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateActivityService():

    def __init__(self, company: Companies, speaker: Speakers, payload: Dict):
        self.name = payload.get('name')
        self.description = payload.get('description')
        self.location = payload.get('location')
        self.datetime = payload.get('datetime')
        self.type = payload.get('type')
        self.registration_open = payload.get('registration_open')
        self.registration_link = payload.get('registration_link')
        self.company = company
        self.speaker = speaker

    def call(self) -> Optional[Activities]:
        
        activity = Activities.create(
            name=self.name,
            description=self.description,
            location=self.location,
            datetime=self.datetime,
            type=self.type,
            registration_open=self.registration_open,
            registration_link=self.registration_link,
        )

        if not activity:
            return None

        if self.company:
            try:
                # add new activity to a company
                self.company.agents.append(activity)
                self.company.save()
            except Exception:
                logger.exception('Failed to add new activity to company')
                return None
        
        if self.speaker:
            try:
                # add new activity to a speaker
                self.speaker.agents.append(activity)
                self.speaker.save()
            except Exception:
                logger.exception('Failed to add new activity to speaker')
                return None

        return activity

