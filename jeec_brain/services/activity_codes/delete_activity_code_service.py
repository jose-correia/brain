from jeec_brain.models.activity_codes import ActivityCodes


class DeleteActivityCodeService:
    def __init__(self, activity_code: ActivityCodes):
        self.activity_code = activity_code

    def call(self) -> bool:
        result = self.activity_code.delete()
        return result
