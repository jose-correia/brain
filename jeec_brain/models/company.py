from jeec_brain.database import db
from jeec_brain.database.model import ModelMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Company(ModelMixin, db.Model, UserMixin):
    __tablename__ = 'company'
    
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))

    password_hash = db.Column(db.String(128))
    
    def __init__(self, name, username):
        self.name = name
        self.username = username

    def __repr__(self):
        return '<Username: {}  |  Name: {}>'.format(self.username, self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)