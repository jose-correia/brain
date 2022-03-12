from typing import Dict, Optional
from jeec_brain.models.activity_types import ActivityTypes


class UpdateActivityTypeService:
    def __init__(self, activity_type: ActivityTypes, kwargs: Dict):
        self.activity_type = activity_type
        self.kwargs = kwargs

    def call(self) -> Optional[ActivityTypes]:
        update_result = self.activity_type.update(**self.kwargs)
        return update_result
