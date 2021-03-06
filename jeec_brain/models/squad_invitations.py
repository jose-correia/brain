from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class SquadInvitations(db.Model, ModelMixin):
    __tablename__ = 'squad_invitations'
    
    __table_args__ = (db.UniqueConstraint('sender_id', 'receiver_id', name='uix_squads'),)

    sender_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), index=True)