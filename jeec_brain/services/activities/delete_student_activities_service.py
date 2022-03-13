from jeec_brain.models.student_activities import StudentActivities


class DeleteStudentActivityService:
    def __init__(self, student_activity: StudentActivities):
        self.student_activity = student_activity

    def call(self) -> bool:
        result = self.student_activity.delete()
        return result
