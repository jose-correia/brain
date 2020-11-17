from typing import Optional
from jeec_brain.models.student_activities import StudentActivities


class AddStudentActivityService():
    def __init__(self, student_id: int, activity_id: int, quest: bool, done: bool):
        self.student_id = student_id
        self.activity_id = activity_id
        self.quest = quest
        self.done = done

    def call(self) -> Optional[StudentActivities]:
        student_activity = StudentActivities.create(
            student_id=self.student_id,
            activity_id=self.activity_id,
            quest=self.quest,
            done=self.done
        )
        return student_activity
