from jeec_brain.models.activities_tags import ActivitiesTags


class DeleteActivityTagService:
    def __init__(self, activity_tag: ActivitiesTags):
        self.activity_tag = activity_tag

    def call(self) -> bool:
        result = self.activity_tag.delete()
        return result
