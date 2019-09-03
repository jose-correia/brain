from jeec_brain.models.users import Users

class CreateUserService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        user = Users(**self.kwargs)
        
        user.create()
        user.reload()
        
        return user