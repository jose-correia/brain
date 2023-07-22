import logging
from jeec_brain.models.student_daily_points import StudentDailyPoints
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateStudentDailyPointsService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[StudentDailyPoints]:

        student_daily_points = StudentDailyPoints.create(**self.kwargs)

        if not student_daily_points:
            return None

        return student_daily_points
