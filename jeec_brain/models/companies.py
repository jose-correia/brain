from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class Companies(db.Model, ModelMixin):
    __tablename__ = 'companies'
    
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))

    link = db.Column(db.String(100))

    password_hash = db.Column(db.String(128))

    user = relationship('Users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    access_cv_platform = db.Column(db.Boolean, default=False)
    
    activities = relationship("Activities", back_populates='company', lazy='dynamic')
    
    business_area = db.Column(db.String(100))


    def __repr__(self):
        return 'Name: {} | CV_Platform access: {}'.format(self.name, self.access_cv_platform)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def give_cv_access(self):
        self.access_cv_platform = True
        db.session.commit()
    
    def remove_cv_access(self):
        self.access_cv_platform = False
        db.session.commit()
