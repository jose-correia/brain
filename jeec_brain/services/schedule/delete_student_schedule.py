from jeec_brain.models.student_schedule import ScheduleStudent


class DeleteScheduleStudentService:
    def __init__(self, schedule_student: ScheduleStudent):
        self.schedule_student = schedule_student

    def call(self) -> bool:
        result = self.schedule_student.delete()
        return result
