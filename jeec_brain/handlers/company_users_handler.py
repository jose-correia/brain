# SERVICES
from jeec_brain.services.company_users.create_company_user_service import (
    CreateCompanyUserService,
)
from jeec_brain.services.company_users.delete_company_user_service import (
    DeleteCompanyUserService,
)
from jeec_brain.services.company_users.update_company_user_service import (
    UpdateCompanyUserService,
)
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)
from jeec_brain.models.enums.roles_enum import RolesEnum

# HANDLERS
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.activities_handler import ActivitiesHandler


class CompanyUsersHandler:
    @classmethod
    def create_company_user(
        cls, chat_enabled, name, username, email, company, post, food_manager, password
    ):
        # password = GenerateCredentialsService().call()

        if chat_enabled:
            chat_id = UsersHandler.create_chat_user(
                name, username, email, password, "Company"
            )
            if not chat_id:
                return None
        else:
            chat_id = None

        # user = UsersHandler.create_user(
        #     name, username, RolesEnum["company"], email, password, chat_id
        # )
        user = UsersHandler.create_user(
            name, username, "company", email, password, chat_id
        )
        if not user:
            return None

        company_user = CreateCompanyUserService(
            user_id=user.id, company_id=company.id, post=post, food_manager=food_manager
        ).call()

        if chat_enabled:
            if not UsersHandler.join_channel(
                company_user.user, company.chat_id, company.chat_code
            ):
                CompanyUsersHandler.delete_company_user(chat_enabled, company_user)
                return None

            for activity in company_user.company.activities:
                if activity.chat_id:
                    if not ActivitiesHandler.join_channel(company_user.user, activity):
                        CompanyUsersHandler.delete_company_user(
                            chat_enabled, company_user
                        )
                        return None

        return company_user

    @classmethod
    def delete_company_user(cls, chat_enabled, company_user):
        if chat_enabled and company_user.user.chat_id:
            result = DeleteChatUserService(company_user.user).call()
            if not result:
                return False

        return DeleteCompanyUserService(company_user=company_user).call()

    @classmethod
    def update_company_user(cls, company_user, **kwargs):
        return UpdateCompanyUserService(company_user=company_user, kwargs=kwargs).call()
