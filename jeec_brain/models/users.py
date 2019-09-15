from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from flask_login import UserMixin
from datetime import datetime


class Users(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)

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