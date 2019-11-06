from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from flask_login import UserMixin
from datetime import datetime
from jeec_brain.models.enums.roles_enum import RolesEnum
# from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100))

    password = db.Column(db.String)
    
    role = db.Column(db.Enum(RolesEnum), nullable=False)

    company = db.relationship('Companies', back_populates="users", uselist=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    sent_authentication_to_email = db.Column(db.Boolean, default=False)
    last_auth_email_destination = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        """
        Method used by Flask-Login to be used on user_loader callback. We want to use Argonath Session Token here.
        :return:
        """
        return self.username
    
    def get_role(self):
        return self.role
