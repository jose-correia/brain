from typing import Dict, Optional
from jeec_brain.models.student_activities import StudentActivities


class UpdateStudentActivitiesService():
    
    def __init__(self, student_activity: StudentActivities, kwargs: Dict):
        self.student_activity = student_activity
        self.kwargs = kwargs

    def call(self) -> Optional[StudentActivities]:
        update_result = self.student_activity.update(**self.kwargs)
        return update_result
