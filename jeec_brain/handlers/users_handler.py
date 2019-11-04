# SERVICES
from jeec_brain.services.users.create_user_service import CreateUserService
from jeec_brain.services.users.delete_user_service import DeleteUserService
from jeec_brain.services.users.update_user_service import UpdateUserService
from jeec_brain.services.users.generate_credentials_service import GenerateCredentialsService


class UsersHandler():

    @classmethod
    def create_user(cls, **kwargs):
        return CreateUserService(kwargs=kwargs).call()

    @classmethod
    def delete_user(cls, user):
        return DeleteUserService(user=user).call()

    @classmethod
    def generate_new_user_credentials(cls, user):
        try:            
            data = {
                'password': GenerateCredentialsService().call()
            }
            updated = UpdateUserService(user=user, kwargs=data).call()
        except:
            return None

        if updated is None:
            return False
            
        return True
