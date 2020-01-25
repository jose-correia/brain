from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompanyResumeSubmissions(db.Model, ModelMixin):
    __tablename__ = 'company_resume_submissions'

    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    resume_submission_id = Column(Integer, ForeignKey('resume_submissions.id'), index=True)
