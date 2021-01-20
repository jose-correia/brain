from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompanyActivities(db.Model, ModelMixin):
    __tablename__ = 'company_activities'

    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    activity_id = Column(Integer, ForeignKey('activities.id'), index=True)
    zoom_link = db.Column(db.String)