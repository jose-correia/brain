# SERVICES
from jeec_brain.services.users.create_user_service import CreateUserService
from jeec_brain.services.users.delete_user_service import DeleteUserService
from jeec_brain.services.users.update_user_service import UpdateUserService
from jeec_brain.services.users.generate_credentials_service import GenerateCredentialsService
from jeec_brain.services.chat.create_chat_user_service import CreateChatUserService
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.services.chat.login_chat_user_service import LoginChatUserService


class UsersHandler():

    @classmethod
    def create_user(cls, username, role, company_id=None, email=None, password=None, food_manager=None, chat_id=None):
        return CreateUserService(
            company_id=company_id,
            username=username,
            email=email,
            password=password,
            role=role,
            food_manager=food_manager,
            chat_id=chat_id
        ).call()

    @classmethod
    def delete_user(cls, user):
        if user.chat_id:
            result = DeleteChatUserService(user).call()
            if not result:
                return False

        return DeleteUserService(user=user).call()

    @classmethod
    def update_user(cls, user, **kwargs):
        return UpdateUserService(user=user, kwargs=kwargs).call()

    @classmethod
    def generate_new_user_credentials(cls, user):
        try:            
            data = {
                'password': GenerateCredentialsService().call()
            }
            updated = UpdateUserService(user=user, kwargs=data).call()
        except:
            return False

        if updated is None:
            return False
            
        return True

    @classmethod
    def create_chat_user(cls, name, username, email, password, role):
        return CreateChatUserService({"name":name, "email":email, "username":username, "password":password, "roles":[role]}).call()

    @classmethod
    def get_chat_user_token(cls, user):
        chat_user = LoginChatUserService(user.username, user.password).call()
        
        if chat_user:
            return chat_user['authToken']
        else:
            return None
