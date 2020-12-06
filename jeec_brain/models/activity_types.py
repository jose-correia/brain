from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class ActivityTypes(db.Model, ModelMixin):
    __tablename__ = 'activity_types'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float())

    show_in_home = db.Column(db.Boolean, default=True)
    show_in_schedule = db.Column(db.Boolean, default=True)
    show_in_app = db.Column(db.Boolean, default=True)

    event = relationship('Events', back_populates="activity_types", uselist=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    activities = relationship("Activities", back_populates='activity_type', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return 'Name: {}  |  Price: {}'.format(self.name, self.price)
