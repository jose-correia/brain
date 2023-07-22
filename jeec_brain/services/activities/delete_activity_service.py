from jeec_brain.models.activities import Activities


class DeleteActivityService:
    def __init__(self, activity: Activities):
        self.activity = activity

    def call(self) -> bool:
        result = self.activity.delete()
        return result
