# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService
from jeec_brain.services.students.update_student_service import UpdateStudentService
from jeec_brain.services.students.add_student_company_service import AddStudentCompanyService
from jeec_brain.services.students.delete_student_company_service import DeleteStudentCompanyService
from jeec_brain.services.students.update_student_company_service import UpdateStudentCompanyService
from jeec_brain.services.students.add_student_login_service import AddStudentLoginService
from jeec_brain.services.students.delete_student_login_service import DeleteStudentLoginService
from jeec_brain.services.students.update_student_login_service import UpdateStudentLoginService
from jeec_brain.services.students.create_banned_student_service import CreateBannedStudentService
from jeec_brain.services.students.delete_banned_student_service import DeleteBannedStudentService
from jeec_brain.services.students.update_banned_student_service import UpdateBannedStudentService
from jeec_brain.services.users.generate_credentials_service import GenerateCredentialsService
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.models.enums.roles_enum import RolesEnum

# FINDERS
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder

# HANDLERS
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.squads_handler import SquadsHandler

class StudentsHandler():

    @classmethod
    def create_student(cls, name, ist_id, email, course, entry_year, fenix_auth_code, photo, photo_type):
        password = GenerateCredentialsService().call()
        referral_code = GenerateCredentialsService().call()

        chat_id = UsersHandler.create_chat_user(name, ist_id, email, password, 'Student')
        if not chat_id:
            return None

        user = UsersHandler.create_user(name, ist_id, RolesEnum['student'], email, password, chat_id)
        if not user:
            return None

        return CreateStudentService(
            user_id=user.id,
            course=course,
            entry_year=entry_year,
            referral_code=referral_code,
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
        if student.user.chat_id:
            result = DeleteChatUserService(student.user).call()
            if not result:
                return False

        return DeleteStudentService(student=student).call()

    @classmethod
    def update_student(cls, student, **kwargs):
        return UpdateStudentService(student=student, kwargs=kwargs).call()

    @classmethod
    def add_points(cls, student, points):
        student.daily_points += points
        student.total_points += points
        student.squad_points += points

        while(student.total_points > student.level.points):
            level = LevelsFinder.get_level_by_value(student.level.value + 1)
            if(level is not None):
                student.level = level

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
            SquadsHandler.update_squad(student.squad, captain_ist_id=student.squad.members.first().user.username)

        invitations = SquadsFinder.get_invitations_from_parameters({'sender_id': student.id})
        for invitation in invitations:
            SquadsHandler.delete_squad_invitation(invitation)

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

    @classmethod
    def add_student_company(cls, student, company):
        return AddStudentCompanyService(student.id, company.id).call()
    
    @classmethod
    def update_student_company(cls, student_company, **kwargs):
        return UpdateStudentCompanyService(student_company, kwargs).call()

    @classmethod
    def delete_student_company(cls, student_company):
        return DeleteStudentCompanyService(student_company).call()

    @classmethod
    def add_student_login(cls, student, date):
        return AddStudentLoginService(student.id, date).call()
    
    @classmethod
    def update_student_login(cls, student_login, **kwargs):
        return UpdateStudentLoginService(student_login, kwargs).call()

    @classmethod
    def delete_student_login(cls, student_login):
        return DeleteStudentLoginService(student_login).call()

    @classmethod
    def create_banned_student(cls, student):
        return CreateBannedStudentService(name=student.user.name, ist_id=student.user.username, email=student.user.email).call()

    @classmethod
    def update_banned_student(cls, banned_student, **kwargs):
        return UpdateBannedStudentService(banned_student, kwargs).call()

    @classmethod
    def delete_banned_student(cls, banned_student):
        return DeleteBannedStudentService(banned_student).call()

    # @classmethod
    # def upload_student_cv(cls, file, username):
    #     return UploadImageService(file, username, 'static/cv_platform/cvs').call()