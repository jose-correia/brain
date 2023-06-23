# SERVICES
from jeec_brain.services.activities.create_activity_service import CreateActivityService
from jeec_brain.services.activities.update_activity_service import UpdateActivityService
from jeec_brain.services.activities.delete_activity_service import DeleteActivityService
from jeec_brain.services.activities.add_company_activity_service import (
    AddCompanyActivityService,
)
from jeec_brain.services.activities.update_company_activities_service import (
    UpdateCompanyActivityService,
)
from jeec_brain.services.activities.delete_company_activities_service import (
    DeleteCompanyActivityService,
)
from jeec_brain.services.activities.add_speaker_activity_service import (
    AddSpeakerActivityService,
)
from jeec_brain.services.activities.update_speaker_activities_service import (
    UpdateSpeakerActivityService,
)
from jeec_brain.services.activities.delete_speaker_activities_service import (
    DeleteSpeakerActivityService,
)
from jeec_brain.services.activities.add_student_activity_service import (
    AddStudentActivityService,
)
from jeec_brain.services.activities.update_student_activities_service import (
    UpdateStudentActivitiesService,
)
from jeec_brain.services.activities.delete_student_activities_service import (
    DeleteStudentActivityService,
)
from jeec_brain.services.chat.create_channel_service import CreateChannelService
from jeec_brain.services.chat.delete_channel_service import DeleteChannelService
from jeec_brain.services.chat.join_channel_service import JoinChannelService

# FINDERS
from jeec_brain.finders.students_finder import StudentsFinder

# HANDLERS
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.students_handler import StudentsHandler

from config import Config


class ActivitiesHandler:
    @classmethod
    def create_activity(cls, chat_enabled, event, activity_type, chat=False, **kwargs):
        if chat_enabled and chat:
            chat_id, chat_code = CreateChannelService(
                name=kwargs.get("name", None)
            ).call()
            if not chat_id or not chat_code:
                return None
        else:
            chat_id = None
            chat_code = None

        return CreateActivityService(
            event=event,
            activity_type=activity_type,
            kwargs={**kwargs, **{"chat_id": chat_id, "chat_code": chat_code}},
        ).call()

    @classmethod
    def update_activity(
        cls, chat_enabled, activity, activity_type, chat=False, **kwargs
    ):
        if chat_enabled:
            if activity.chat_id and not chat:
                result = DeleteChannelService(activity.chat_id).call()
                if not result:
                    return None
                else:
                    return UpdateActivityService(
                        activity=activity,
                        activity_type=activity_type,
                        kwargs={**kwargs, **{"chat_id": None, "chat_code": None}},
                    ).call()

            elif not activity.chat_id and chat:
                chat_id, chat_code = CreateChannelService(
                    name=kwargs.get("name", None)
                ).call()
                if not chat_id or not chat_code:
                    return None

                return UpdateActivityService(
                    activity=activity,
                    activity_type=activity_type,
                    kwargs={**kwargs, **{"chat_id": chat_id, "chat_code": chat_code}},
                ).call()

        return UpdateActivityService(
            activity=activity, activity_type=activity_type, kwargs=kwargs
        ).call()

    @classmethod
    def delete_activity(cls, chat_enabled, activity):
        if chat_enabled and activity.chat_id:
            result = DeleteChannelService(activity.chat_id).call()
            if not result:
                return False

        return DeleteActivityService(activity=activity).call()

    @classmethod
    def add_speaker_activity(cls, speaker, activity):
        return AddSpeakerActivityService(speaker.id, activity.id).call()

    @classmethod
    def update_speaker_activity(cls, speaker_activity, speaker, activity):
        return UpdateSpeakerActivityService(
            speaker_activity, speaker.id, activity.id
        ).call()

    @classmethod
    def delete_speaker_activities(cls, speaker_activity):
        return DeleteSpeakerActivityService(speaker_activity).call()

    @classmethod
    def add_company_activity(cls, chat_enabled, company, activity):
        if chat_enabled and activity.chat_id:
            for company_user in company.users:
                user = company_user.user
                if not user.chat_id:
                    chat_id = UsersHandler.create_chat_user(
                        user.username,
                        user.username,
                        user.email,
                        user.password,
                        "Company",
                    )
                    if not chat_id:
                        return None
                    user = UsersHandler.update_user(user, chat_id=chat_id)
                    if user is None:
                        return None

                result = cls.join_channel(user, activity)
                if not result:
                    return None

        return AddCompanyActivityService(company.id, activity.id).call()

    @classmethod
    def update_company_activity(cls, company_activity, company, activity):
        return UpdateCompanyActivityService(
            company_activity, company.id, activity.id
        ).call()

    @classmethod
    def delete_company_activities(cls, company_activity):
        return DeleteCompanyActivityService(company_activity).call()

    @classmethod
    def add_student_activity(cls, student, activity, code, company=None):
        company_id = (
            company.id if (company is not None) else None
        )
        student_activity = AddStudentActivityService(
            student.id, activity.id, code, company_id
        ).call()
        if student_activity:
            if (
                len(StudentsFinder.get_student_activities_from_student_id(student.id))
                == 1
            ):
                referral = StudentsFinder.get_referral_redeemer(student)
                if referral:
                    redeemed = StudentsFinder.get_from_id(referral.redeemed_id)
                    StudentsHandler.add_points(redeemed, Config.REWARD_REFERRAL)
            return student_activity
        return None

    @classmethod
    def update_student_activity(cls, student_activity, **kwargs):
        return UpdateStudentActivitiesService(student_activity, kwargs).call()

    @classmethod
    def delete_student_activity(cls, student_activity):
        return DeleteStudentActivityService(student_activity).call()

    @classmethod
    def join_channel(cls, user, activity):
        return JoinChannelService(user, activity.chat_id, activity.chat_code).call()
