from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class StudentReferrals(db.Model, ModelMixin):
    __tablename__ = 'student_referrals'
    
    redeemed_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), index=True)
    redeemer_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), index=True, unique=True)