from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Events(db.Model, ModelMixin):
    __tablename__ = "events"

    name = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))

    default = db.Column(db.Boolean, default=False)

    email = db.Column(db.String(100))
    location = db.Column(db.String(100))

    facebook_link = db.Column(db.String(100))
    facebook_event_link = db.Column(db.String(100))
    youtube_link = db.Column(db.String(100))
    instagram_link = db.Column(db.String(100))

    show_schedule = db.Column(db.Boolean, default=False)
    show_registrations = db.Column(db.Boolean, default=False)
    show_prizes = db.Column(db.Boolean, default=False)

    cvs_submission_start = db.Column(db.String(30))
    cvs_submission_end = db.Column(db.String(30))
    cvs_access_start = db.Column(db.String(30))
    cvs_access_end = db.Column(db.String(30))
    cvs_purged = db.Column(db.Boolean, default=False)

    end_game_day = db.Column(db.String(20))
    end_game_time = db.Column(db.String(10))

    activity_types = relationship(
        "ActivityTypes",
        back_populates="event",
        lazy="dynamic",
        cascade="all,delete",
        order_by="ActivityTypes.name",
    )
    activities = relationship(
        "Activities",
        back_populates="event",
        lazy="dynamic",
        cascade="all,delete",
        order_by="Activities.day, Activities.time",
    )
    teams = relationship(
        "Teams",
        back_populates="event",
        lazy="dynamic",
        cascade="all,delete",
        order_by="Teams.website_priority",
    )

    def __repr__(self):
        return "Name: {} | date: {}".format(self.name, self.start_date)
