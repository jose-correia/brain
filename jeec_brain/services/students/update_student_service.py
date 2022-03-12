from typing import Dict, Optional
from jeec_brain.models.students import Students


class UpdateStudentService:
    def __init__(self, student: Students, kwargs: Dict):
        self.student = student
        self.kwargs = kwargs

    def call(self) -> Optional[Students]:
        try:
            update_result = self.student.update(**self.kwargs)
        except:
            return None

        return update_result
