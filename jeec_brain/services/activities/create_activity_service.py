import logging
from jeec_brain.models.activities import Activities
from jeec_brain.models.activity_types import ActivityTypes
from jeec_brain.models.events import Events
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateActivityService:
    def __init__(self, event: Events, activity_type: ActivityTypes, kwargs: Dict):
        self.kwargs = kwargs
        self.event = event
        self.activity_type = activity_type

    def call(self) -> Optional[Activities]:

        activity = Activities.create(**self.kwargs)

        if not activity:
            return None

        try:
            self.activity_type.activities.append(activity)
            self.activity_type.save()
        except Exception as e:
            logger.exception("Failed to add new activity to type. " + str(e))
            return None

        try:
            self.event.activities.append(activity)
            self.event.save()
        except Exception:
            logger.exception("Failed to add new activity to event. " + str(e))
            return None

        return activity
