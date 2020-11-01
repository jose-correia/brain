# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService
from jeec_brain.services.students.update_student_service import UpdateStudentService


class StudentsHandler():

    @classmethod
    def create_student(cls, ist_id, name, user_id, fenix_auth_code, photo, photo_type):
        return CreateStudentService(
            ist_id=ist_id,
            name=name,
            user_id=user_id,
            fenix_auth_code=fenix_auth_code,
            photo=photo,
            photo_type=photo_type
        ).call()

    @classmethod
    def delete_student(cls, student):
        return DeleteStudentService(student=student).call()

    @classmethod
    def update_student(cls, student, **kwargs):
        return UpdateStudentService(student=student, kwargs=kwargs).call()
