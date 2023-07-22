from jeec_brain.models.student_schedule import ScheduleStudent

class ScheduleStudentFinder:
    @classmethod
    def get_from_student_id(cls, student_id):
        return ScheduleStudent.query.filter_by(student_id=student_id).first()