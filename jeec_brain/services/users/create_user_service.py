from jeec_brain.models.users import Users


class CreateUserService():

    def __init__(self, username, role):
        self.username = username
        self.role = role

    def call(self) -> Optional[Users]:
        user = Users.create(username=self.username, role=self.role)
        
        if not user:
            return None

        return user
