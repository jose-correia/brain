from jeec_brain.models.users import Users


class UsersFinder():
    
    @classmethod
    def get_user_from_credentials(cls, username, password):
        return Users.get_by(username=username, password=password)

    @classmethod
    def get_from_external_id(cls, external_id):
        return Users.get_by(external_id=external_id)

    @classmethod
    def get_user_from_username(cls, username):
        return Users.get_by(username=username)

    @classmethod
    def get_users_by_role(cls, role):
        return Users.get_by(role=role)

    @classmethod
    def get_all(cls):
        return Users.all()

    @classmethod
    def search_by_username(cls, username):
        search = "%{}%".format(username)
        return Users.query.filter(Users.username.ilike(search)).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            users = Users.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return users
    
    