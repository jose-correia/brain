from jeec_brain.models.users import Users
from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.models.students import Students


class UsersFinder:
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
    def get_all_admin_users(cls):
        return Users.query.filter(
            (Users.role != "student") & (Users.role != "company")
        ).all()

    @classmethod
    def search_by_username(cls, username):
        search = "%{}%".format(username)
        return Users.query.filter(Users.username.ilike(search)).all()

    @classmethod
    def get_admin_users_by_username(cls, username):
        search = "%{}%".format(username)
        return Users.query.filter(
            Users.username.ilike(search)
            & (Users.role != "student")
            & (Users.role != "company")
        ).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            users = Users.query.filter_by(**kwargs).all()
        except Exception:
            return None

        return users

    @classmethod
    def get_admin_users_from_parameters(cls, kwargs):
        try:
            users = (
                Users.query.filter_by(**kwargs)
                .filter(Users.role != "student" & Users.role != "company")
                .all()
            )
        except Exception:
            return None

        return users

    @classmethod
    def get_from_fenix_auth_code(cls, fenix_auth_code):
        student = Students.query.filter_by(fenix_auth_code=fenix_auth_code).first()

        if student is None or student.user is None:
            return None
        else:
            return student.user

    @classmethod
    def get_all_company_users(cls):
        return CompanyUsers.all()

    @classmethod
    def get_company_user_from_user(cls, user):
        return CompanyUsers.query.filter_by(user_id=user.id).first()

    @classmethod
    def get_company_users_from_username(cls, username):
        return CompanyUsers.query.filter(CompanyUsers.user.username == username).all()
