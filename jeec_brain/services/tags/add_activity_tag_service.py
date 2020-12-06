from typing import Optional
from jeec_brain.models.activities_tags import ActivitiesTags

class AddActivityTagService(object):
    def __init__(self, activity_id, tag_id):
        self.activity_id = activity_id
        self.tag_id = tag_id

    def call(self) -> Optional[ActivitiesTags]:
        activity_tag = ActivitiesTags.create(
            activity_id=self.activity_id,
            tag_id=self.tag_id
        )
        return activity_tag