from jeec_brain.models.users import Users

class CreateUserService():
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def call(self):
        user = Users(username=self.username, role=self.role)
        
        user.create()
        user.reload()
        
        return user