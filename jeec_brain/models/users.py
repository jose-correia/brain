from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from flask_login import UserMixin
# from jeec_brain.models.enums.roles_enum2 import RolesEnum2

# from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model, ModelMixin, UserMixin):
    __tablename__ = "users"

    name = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String)

    role = db.Column(db.String, nullable=False)

    sent_authentication_to_email = db.Column(db.Boolean, default=False)
    last_auth_email_destination = db.Column(db.String(100))

    accepted_terms = db.Column(db.Boolean, default=False)

    chat_id = db.Column(db.String)

    def __repr__(self):
        return "<User %r>" % self.username

    def get_id(self):
        """
        Method used by Flask-Login to be used on user_loader callback. We want to use Argonath Session Token here.
        :return:
        """
        return self.username

    def get_role(self):
        return self.role
