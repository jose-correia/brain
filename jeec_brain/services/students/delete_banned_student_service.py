from jeec_brain.models.banned_students import BannedStudents


class DeleteBannedStudentService:
    def __init__(self, banned_student: BannedStudents):
        self.banned_student = banned_student

    def call(self) -> bool:
        result = self.banned_student.delete()
        return result
