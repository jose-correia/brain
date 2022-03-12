# SERVICES
from jeec_brain.services.users.create_user_service import CreateUserService
from jeec_brain.services.users.delete_user_service import DeleteUserService
from jeec_brain.services.users.update_user_service import UpdateUserService
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)
from jeec_brain.services.chat.create_chat_user_service import CreateChatUserService
from jeec_brain.services.chat.delete_chat_user_service import DeleteChatUserService
from jeec_brain.services.chat.login_chat_user_service import LoginChatUserService
from jeec_brain.services.chat.join_channel_service import JoinChannelService
from jeec_brain.services.chat.create_direct_message_service import (
    CreateDirectMessageService,
)


class UsersHandler:
    @classmethod
    def create_user(cls, name, username, role, email=None, password=None, chat_id=None):
        return CreateUserService(
            name=name,
            username=username,
            email=email,
            password=password,
            role=role,
            chat_id=chat_id,
        ).call()

    @classmethod
    def delete_user(cls, chat_enabled, user):
        if chat_enabled and user.chat_id:
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
            data = {"password": GenerateCredentialsService().call()}
            updated = UpdateUserService(user=user, kwargs=data).call()
        except:
            return False

        if updated is None:
            return False

        return True

    @classmethod
    def create_chat_user(cls, name, username, email, password, role):
        return CreateChatUserService(
            {
                "name": name,
                "email": email,
                "username": username,
                "password": password,
                "roles": [role],
            }
        ).call()

    @classmethod
    def get_chat_user_token(cls, user):
        chat_user = LoginChatUserService(user.username, user.password).call()

        if chat_user:
            return chat_user["authToken"]
        else:
            return ""

    @classmethod
    def join_channel(cls, user, chat_id, chat_code):
        return JoinChannelService(user, chat_id, chat_code).call()

    @classmethod
    def create_direct_message(cls, user_sender, user_receiver):
        return CreateDirectMessageService(user_sender, user_receiver).call()
