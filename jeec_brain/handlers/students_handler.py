# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService


class StudentsHandler():

    @classmethod
    def create_student(cls, name, ist_id, user_id=None):
        return CreateStudentService(
            name=name,
            ist_id=ist_id,
            user_id=user_id
        ).call()

    @classmethod
    def delete_student(cls, student):
        return DeleteStudentService(student=student).call()
