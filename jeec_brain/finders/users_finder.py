from jeec_brain.models.users import Users


class UsersFinder():
    
    @classmethod
    def get_user_from_request(cls, request):
        auth = request.headers["AUTHORIZATION"]
        username, api_key = auth.splot()[1].split(":")
        return Users.get_by(username=username)

    @classmethod
    def get_username_from_id(cls, user_id):
        return Users.get(user_id)

    @classmethod
    def get_user_from_username(cls, username):
        return Users.get_by(username=username)

    @classmethod
    def get_all(cls):
        return Users.all()
    