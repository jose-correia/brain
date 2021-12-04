# SERVICES
from jeec_brain.services.company_users.create_company_user_service import CreateCompanyUserService
from jeec_brain.services.company_users.delete_company_user_service import DeleteCompanyUserService
from jeec_brain.services.company_users.update_company_user_service import UpdateCompanyUserService
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.services.users.generate_credentials_service import GenerateCredentialsService
from jeec_brain.models.enums.roles_enum import RolesEnum

# HANDLERS
from jeec_brain.handlers.users_handler import UsersHandler

class CompanyUsersHandler():

    @classmethod
    def create_company_user(cls, name, username, email, company_id, post, food_manager, evf_username, evf_password):
        password = GenerateCredentialsService().call()
        
        # chat_id = UsersHandler.create_chat_user(name, username, email, password, 'Company')
        # if not chat_id:
        #     return None

        user = UsersHandler.create_user(name, username, RolesEnum['company'], email, password, None)
        if not user:
            return None

        return CreateCompanyUserService(
            user_id=user.id,
            company_id=company_id,
            post=post,
            food_manager=food_manager,
            evf_username=evf_username,
            evf_password=evf_password
        ).call()

    @classmethod
    def delete_company_user(cls, company_user):
        if company_user.user.chat_id:
            result = DeleteChatUserService(company_user.user).call()
            if not result:
                return False

        return DeleteCompanyUserService(company_user=company_user).call()

    @classmethod
    def update_company_user(cls, company_user, **kwargs):
        return UpdateCompanyUserService(company_user=company_user, kwargs=kwargs).call()

  