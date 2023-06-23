from typing import Dict, Optional
from jeec_brain.models.student_schedule import ScheduleStudent


class UpdateScheduleStudentService:
    def __init__(self, schedule_student: ScheduleStudent, kwargs: Dict):
        self.schedule_student = schedule_student
        self.kwargs = kwargs

    def call(self) -> Optional[ScheduleStudent]:
        update_result = self.schedule_student.update(**self.kwargs)
        return update_result
