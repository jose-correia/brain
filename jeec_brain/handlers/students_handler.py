# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService
from jeec_brain.services.students.update_student_service import UpdateStudentService

# FINDERS
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.students_finder import StudentsFinder

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

    @classmethod
    def invite_squad_members(cls, student, members_ist_id):
        if(student.squad is None or (len(members_ist_id) + len(student.squad.members.all()) > 4)):
            return None

        for member_ist_id in members_ist_id:
            member = StudentsFinder.get_from_ist_id(member_ist_id)
            if(member is None or member in student.squad.members):
                continue

            if(SquadsHandler.create_squad_invitation(sender_id=student.id,receiver_id=member.id) is None):
                return False

        return True

    @classmethod
    def leave_squad(cls, student):
        if(student.squad is None):
            return student
        
        if(len(student.squad.members.all()) == 1 ):
            SquadsHandler.delete_squad(student.squad)

        elif(student.is_captain()):
            SquadsHandler.update_squad(student.squad, captain_ist_id=student.squad.members.first().ist_id)

        return cls.update_student(student, squad_id=None, squad_points=0)

    @classmethod
    def accept_invitation(cls, student, invitation):
        if(student.id != invitation.receiver_id):
            return False

        sender = StudentsFinder.get_from_id(invitation.sender_id)
        if(student.squad and sender.squad and student.squad.id == sender.squad.id):
            return student

        cls.leave_squad(student)

        SquadsHandler.delete_squad_invitation(invitation)

        return cls.add_squad_member(student, sender.squad)

    # @classmethod
    # def upload_student_cv(cls, file, username):
    #     return UploadImageService(file, username, 'static/cv_platform/cvs').call()
