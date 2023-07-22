from jeec_brain.handlers.reward_student_handler import StudentRewardsHandler
from jeec_brain.finders.student_rewards_finder import StudentRewardsFinder
from config import Config

# SERVICES
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.students.delete_student_service import DeleteStudentService
from jeec_brain.services.students.update_student_service import UpdateStudentService
from jeec_brain.services.students.add_student_company_service import (
    AddStudentCompanyService,
)
from jeec_brain.services.students.delete_student_company_service import (
    DeleteStudentCompanyService,
)
from jeec_brain.services.students.update_student_company_service import (
    UpdateStudentCompanyService,
)
from jeec_brain.services.students.create_student_referral_service import (
    CreateStudentReferralService,
)
from jeec_brain.services.students.update_student_referral_service import (
    UpdateStudentReferralService,
)
from jeec_brain.services.students.delete_student_referral_service import (
    DeleteStudentReferralService,
)
from jeec_brain.services.students.create_student_daily_points_service import (
    CreateStudentDailyPointsService,
)
from jeec_brain.services.students.update_student_daily_points_service import (
    UpdateStudentDailyPointsService,
)
from jeec_brain.services.students.delete_student_daily_points_service import (
    DeleteStudentDailyPointsService,
)
from jeec_brain.services.students.add_student_login_service import (
    AddStudentLoginService,
)
from jeec_brain.services.students.delete_student_login_service import (
    DeleteStudentLoginService,
)
from jeec_brain.services.students.update_student_login_service import (
    UpdateStudentLoginService,
)
from jeec_brain.services.students.create_banned_student_service import (
    CreateBannedStudentService,
)
from jeec_brain.services.students.delete_banned_student_service import (
    DeleteBannedStudentService,
)
from jeec_brain.services.students.update_banned_student_service import (
    UpdateBannedStudentService,
)
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.models.enums.roles_enum import RolesEnum

# FINDERS
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.finders.events_finder import EventsFinder

# HANDLERS
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.squads_handler import SquadsHandler

from datetime import datetime


class StudentsHandler:
    @classmethod
    def create_student(
        cls, chat_enabled, name, ist_id, email, course, entry_year, photo, photo_type
    ):
        password = GenerateCredentialsService().call()
        referral_code = GenerateCredentialsService().call()

        if chat_enabled:
            chat_id = UsersHandler.create_chat_user(
                name, ist_id, email, password, "Student"
            )
            if not chat_id:
                return None
        else:
            chat_id = None

        user = UsersHandler.create_user(
            name, ist_id, "student", email, password, chat_id
        )
        if not user:
            return None

        return CreateStudentService(
            user_id=user.id,
            course=course,
            entry_year=entry_year,
            referral_code=referral_code,
            photo=photo,
            photo_type=photo_type,
            daily_points=0,
            total_points=0,
            squad_points=0,
            level=LevelsFinder.get_level_by_value(1),
        ).call()

    @classmethod
    def delete_student(cls, chat_enabled, student):
        if chat_enabled and student.user.chat_id:
            result = DeleteChatUserService(student.user).call()
            if not result:
                return False

        return DeleteStudentService(student=student).call()

    @classmethod
    def update_student(cls, student, **kwargs):
        return UpdateStudentService(student=student, kwargs=kwargs).call()

    @classmethod
    def add_points(cls, student, points):
        get_reward = True
        event = EventsFinder.get_default_event()
        if not event.end_game_day or not event.end_game_time:
            return student

        now = datetime.utcnow()
        end_game_time = datetime.strptime(
            event.end_game_day + " " + event.end_game_time, "%d %m %Y, %A %H:%M"
        )
        if now > end_game_time:
            return student
        
        if(student.total_points>=student.level.points):
                get_reward = False

        student.daily_points += int(points)
        student.total_points += int(points)
        student.squad_points += int(points)

        if get_reward:
            while student.total_points >= student.level.points:
                level = LevelsFinder.get_level_by_value(student.level.value)
                StudentRewardsHandler.add_reward_student(student=student.id,reward=level.reward_id)
                level = LevelsFinder.get_level_by_value(student.level.value+1)
                if level is not None:
                    student.level = level
                else:
                    break

        if student.squad:
            student.squad.daily_points += int(points)
            student.squad.total_points += int(points)
            SquadsHandler.update_squad(
                student.squad,
                daily_points=student.squad.daily_points,
                total_points=student.squad.total_points,
            )

        return cls.update_student(
            student,
            daily_points=student.daily_points,
            total_points=student.total_points,
            squad_points=student.squad_points,
        )
        
    @classmethod
    def add_squad_member(cls, student, squad):
        return cls.update_student(student, squad_id=squad.id)

    @classmethod
    def invite_squad_members(cls, student, members_ist_id):
        invitations_sent = SquadsFinder.get_invitations_from_parameters(
            {"sender_id": student.id}
        )
        if student.squad is None or (
            len(members_ist_id)
            + len(student.squad.members.all())
            + len(invitations_sent)
            > 4
        ):
            return None

        for member_ist_id in members_ist_id:
            member = StudentsFinder.get_from_ist_id(member_ist_id)
            if member is None or member in student.squad.members:
                continue

            if (
                SquadsHandler.create_squad_invitation(
                    sender_id=student.id, receiver_id=member.id
                )
                is None
            ):
                return False

        return True

    @classmethod
    def leave_squad(cls, student):
        if student.squad is None:
            return student

        if len(student.squad.members.all()) == 1:
            SquadsHandler.delete_squad(student.squad)

        elif student.is_captain():
            SquadsHandler.update_squad(
                student.squad,
                captain_ist_id=list(
                    filter(
                        lambda member: (not member.is_captain()),
                        student.squad.members.all(),
                    )
                )[0].user.username,
            )

        invitations = SquadsFinder.get_invitations_from_parameters(
            {"sender_id": student.id}
        )
        for invitation in invitations:
            SquadsHandler.delete_squad_invitation(invitation)

        return cls.update_student(student, squad_id=None, squad_points=0)

    @classmethod
    def accept_invitation(cls, student, invitation):
        if student.id != invitation.receiver_id:
            return False

        if len(invitation.sender.squad.members.all()) >= 4 or (
            invitation.sender.squad
            and student.squad
            and student.squad.id == invitation.sender.squad.id
        ):
            SquadsHandler.delete_squad_invitation(invitation)
            return False

        SquadsHandler.delete_squad_invitation(invitation)

        cls.leave_squad(student)

        return cls.add_squad_member(student, invitation.sender.squad)

    @classmethod
    def redeem_referral(cls, redeemer, redeemed, code):
        redeemer_code = StudentsFinder.get_referral_redeemer(redeemer)
        if redeemer_code:
            return "Already redeemed a personal code", None
        else:
            referral = CreateStudentReferralService(
                redeemed_id=redeemed.id, redeemer_id=redeemer.id, code=code
            ).call()
            if not referral:
                return "Failed to redeem code", None

            redeemer = cls.add_points(redeemer, int(Config.REWARD_REFERRAL))
           
            cls.add_points(redeemed, int(Config.REWARD_REFERRAL))

            return None, redeemer

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
        return CreateBannedStudentService(
            name=student.user.name,
            ist_id=student.user.username,
            email=student.user.email,
        ).call()

    @classmethod
    def update_banned_student(cls, banned_student, **kwargs):
        return UpdateBannedStudentService(banned_student, kwargs).call()

    @classmethod
    def delete_banned_student(cls, banned_student):
        return DeleteBannedStudentService(banned_student).call()

    @classmethod
    def reset_daily_points(cls, student):
        now = datetime.utcnow()
        date = now.strftime("%d %b %Y, %a")

        if student.daily_points > 0:
            daily_points = CreateStudentDailyPointsService(
                {"student_id": student.id, "points": student.daily_points, "date": date}
            ).call()
            if not daily_points:
                return False

            if not cls.update_student(student, daily_points=0):
                return False

        return True

    # @classmethod
    # def upload_student_cv(cls, file, username):
    #     return UploadImageService(file, username, 'static/cv_platform/cvs').call()

    @classmethod
    def remove_points(cls, student, points):
        event = EventsFinder.get_default_event()
        if not event.end_game_day or not event.end_game_time:
            return student

        now = datetime.utcnow()
        end_game_time = datetime.strptime(
            event.end_game_day + " " + event.end_game_time, "%d %m %Y, %A %H:%M"
        )
        if now > end_game_time:
            return student

        student.daily_points -= int(points)
        student.total_points -= int(points)
        student.squad_points -= int(points)
        if(student.total_points<0):
            return None
        if(student.daily_points<0):
            student.daily_points=0
        if(student.squad_points<0):
            student.squad_points=0
        previous_level = LevelsFinder.get_level_by_value(student.level.value - 1)
        if previous_level != None:
            while student.total_points < previous_level.points:
                student.level = previous_level
                student_reward = StudentRewardsFinder.get_from_student_and_prize(student_id=student.id,reward_id=previous_level.reward_id)
                StudentRewardsHandler.remove_reward_student(student_reward = student_reward[0])
                previous_level = LevelsFinder.get_level_by_value(student.level.value - 1)
                if (previous_level == None):
                    break


        if student.squad:
            student.squad.daily_points -= int(points)
            if(student.squad.daily_points<0):
                student.squad.daily_points=0
            student.squad.total_points -= int(points)
            if(student.squad.total_points<0):
                student.squad.total_points=0
            SquadsHandler.update_squad(
                student.squad,
                daily_points=student.squad.daily_points,
                total_points=student.squad.total_points,
            )

        return cls.update_student(
            student,
            daily_points=student.daily_points,
            total_points=student.total_points,
            squad_points=student.squad_points,
        )
