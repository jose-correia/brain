from flask import current_app
from jeec_brain.models.activity_codes import ActivityCodes
from typing import Dict, Optional


class CreateActivityCodeService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[ActivityCodes]:

        activity_code = ActivityCodes.create(**self.kwargs)

        if not activity_code:
            return None

        return activity_code
