# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService
from jeec_brain.services.students.update_student_service import UpdateStudentService

# FINDERS
from jeec_brain.finders.levels_finder import LevelsFinder

# HANDLERS
from jeec_brain.handlers.squads_handler import SquadsHandler

class StudentsHandler():

    @classmethod
    def create_student(cls, ist_id, name, user_id, fenix_auth_code, photo, photo_type):
        return CreateStudentService(
            ist_id=ist_id,
            name=name,
            user_id=user_id,
            fenix_auth_code=fenix_auth_code,
            photo=photo,
            photo_type=photo_type,
            daily_points=0,
            total_points=0,
            squad_points=0,
            level=LevelsFinder.get_level_by_value(0)
        ).call()

    @classmethod
    def delete_student(cls, student):
        return DeleteStudentService(student=student).call()

    @classmethod
    def update_student(cls, student, **kwargs):
        return UpdateStudentService(student=student, kwargs=kwargs).call()

    @classmethod
    def add_points(cls, student, points):
        student.daily_points += points
        student.total_points += points
        student.squad_points += points

        if(student.squad):
            student.squad.daily_points += points
            student.squad.total_points += points
            SquadsHandler.update_squad(student.squad, daily_points=student.squad.daily_points, total_points=student.squad.total_points)

        return cls.update_student(student, daily_points=student.daily_points, total_points=student.total_points, squad_points=student.squad_points)

    @classmethod
    def add_squad_member(cls, student, squad):
        return cls.update_student(student, squad_id=squad.id)

    @classmethod
    def add_linkedin(cls, student, url):
        return cls.update_student(student, linkedin_url=url)
    
    # @classmethod
    # def upload_student_cv(cls, file, username):
    #     return UploadImageService(file, username, 'static/cv_platform/cvs').call()
