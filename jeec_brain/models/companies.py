from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.users import Users
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.activities import Activities
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Companies(db.Model, ModelMixin):
    __tablename__ = 'companies'
    
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    link = db.Column(db.String(100))
    business_area = db.Column(db.String(100))

    partnership_tier = db.Column(db.String(20))

    show_in_website = db.Column(db.Boolean, default=True)

    activities = relationship("Activities",
        secondary="company_activities",
        secondaryjoin=sql.and_(CompanyActivities.activity_id == Activities.id))

    users = relationship("Users", back_populates='company', lazy='dynamic', cascade="all,delete")
    

    def __repr__(self):
        return 'Name: {} | CV_Platform access: {}'.format(self.name, self.access_cv_platform)
