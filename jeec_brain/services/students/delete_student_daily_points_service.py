from jeec_brain.models.student_daily_points import StudentDailyPoints


class DeleteStudentDailyPointsService():

    def __init__(self, student_daily_points: StudentDailyPoints):
        self.student_daily_points = student_daily_points

    def call(self) -> bool:
        result = self.student_daily_points.delete()
        return result
