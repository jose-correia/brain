from flask import current_app
from typing import Dict, Optional
from jeec_brain.models.activities import Activities
from jeec_brain.models.activity_types import ActivityTypes


class UpdateActivityService:
    def __init__(
        self, activity: Activities, activity_type: ActivityTypes, kwargs: Dict
    ):
        self.activity = activity
        self.kwargs = kwargs
        self.activity_type = activity_type

    def call(self) -> Optional[Activities]:
        update_result = self.activity.update(**self.kwargs)

        try:
            if self.activity not in self.activity_type.activities:
                self.activity_type.activities.append(update_result)
                self.activity_type.save()
        except Exception:
            current_app.logger.exception("Failed to add new activity to type")
            return None

        return update_result
