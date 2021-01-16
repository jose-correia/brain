from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class StudentCompanies(db.Model, ModelMixin):
    __tablename__ = 'student_companies'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), index=True)
