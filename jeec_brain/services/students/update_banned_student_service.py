from typing import Dict, Optional
from jeec_brain.models.banned_students import BannedStudents


class UpdateBannedStudentService:
    def __init__(self, banned_student: BannedStudents, kwargs: Dict):
        self.banned_student = banned_student
        self.kwargs = kwargs

    def call(self) -> Optional[BannedStudents]:
        try:
            update_result = self.banned_student.update(**self.kwargs)
        except:
            return None

        return update_result
