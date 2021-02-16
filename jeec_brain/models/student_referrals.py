from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class StudentReferrals(db.Model, ModelMixin):
    __tablename__ = 'student_referrals'
    
    sender_id = db.Column(db.Integer, db.ForeignKey('students.id'), index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('students.id'), index=True, unique=True)