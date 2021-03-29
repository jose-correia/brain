from typing import Dict, Optional
from jeec_brain.models.student_daily_points import StudentDailyPoints


class UpdateStudentDailyPointsService():
    
    def __init__(self, student_daily_points: StudentDailyPoints, kwargs: Dict):
        self.student_daily_points = student_daily_points
        self.kwargs = kwargs

    def call(self) -> Optional[StudentDailyPoints]:
        update_result = self.student_daily_points.update(**self.kwargs)
        return update_result
