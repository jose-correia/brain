from typing import Optional
from jeec_brain.models.student_activities import StudentActivities


class AddStudentActivityService:
    def __init__(
        self, student_id: int, activity_id: int, code: str, company_id: int = None
    ):
        self.student_id = student_id
        self.activity_id = activity_id
        self.code = code
        self.company_id = company_id

    def call(self) -> Optional[StudentActivities]:
        student_activity = StudentActivities.create(
            student_id=self.student_id,
            activity_id=self.activity_id,
            company_id=self.company_id,
            code=self.code,
        )
        return student_activity
