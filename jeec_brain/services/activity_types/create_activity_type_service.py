from flask import current_app
from jeec_brain.models.activity_types import ActivityTypes
from jeec_brain.models.events import Events
from typing import Dict, Optional


class CreateActivityTypeService:
    def __init__(self, event: Events, kwargs: Dict):
        self.kwargs = kwargs
        self.event = event

    def call(self) -> Optional[ActivityTypes]:

        activity_type = ActivityTypes.create(**self.kwargs)

        if not activity_type:
            return None

        try:
            self.event.activity_types.append(activity_type)
            self.event.save()
        except Exception as error:
            current_app.logger.exception(
                f"Failed to add new activity type to event: {error}"
            )
            return None

        return activity_type
