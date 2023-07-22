import logging
from jeec_brain.models.student_schedule import ScheduleStudent
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateScheduleStudentService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[ScheduleStudent]:

        schedule_student = ScheduleStudent.create(**self.kwargs)

        if not schedule_student:
            return None

        return schedule_student
