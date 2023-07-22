from typing import Dict, Optional
from jeec_brain.models.activities_tags import ActivitiesTags


class UpdateActivityTagService:
    def __init__(self, activity_tag: ActivitiesTags, kwargs: Dict):
        self.activity_tag = activity_tag
        self.kwargs = kwargs

    def call(self) -> Optional[ActivitiesTags]:
        update_result = self.activity_tag.update(**self.kwargs)
        return update_result
