from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.companies import Companies
from jeec_brain.models.company_resume_submissions import CompanyResumeSubmissions
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class ResumeSubmissions(db.Model, ModelMixin):
    __tablename__ = 'resume_submissions'
    
    name = db.Column(db.String(100), nullable=False)

    allow_download = db.Column(db.Boolean, default=False)
    allow_submission = db.Column(db.Boolean, default=False)
    files_purged = db.Column(db.Boolean, default=False)

    participants = relationship("Companies",
        secondary="company_resume_submissions",
        secondaryjoin=sql.and_(CompanyResumeSubmissions.company_id == Companies.id))
   
    def __repr__(self):
        return 'Name: {}'.format(self.name)

