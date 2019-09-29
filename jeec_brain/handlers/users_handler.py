# SERVICES
from jeec_brain.services.users.create_user_service import CreateUserService
from jeec_brain.services.users.delete_user_service import DeleteUserService


class UsersHandler():

    @classmethod
    def create_user(cls, **kwargs):
        return CreateUserService(kwargs=kwargs).call()

    @classmethod
    def delete_user(cls, user):
        return DeleteUserService(user=user).call()
