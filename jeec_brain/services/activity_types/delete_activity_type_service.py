from jeec_brain.models.activity_types import ActivityTypes


class DeleteActivityTypeService():

    def __init__(self, activity_type: ActivityTypes):
        self.activity_type = activity_type

    def call(self) -> bool:
        result = self.activity_type.delete()
        return result
