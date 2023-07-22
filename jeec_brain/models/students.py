from jeec_brain.database import db
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import sql
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.companies import Companies
from jeec_brain.models.squads import Squads
from jeec_brain.models.tags import Tags
from jeec_brain.models.students_tags import StudentsTags
from jeec_brain.models.companies import Companies
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.student_logins import StudentLogins
from jeec_brain.models.activities import Activities
from jeec_brain.models.student_activities import StudentActivities
from jeec_brain.models.levels import Levels


class Students(db.Model, ModelMixin):
    __tablename__ = "students"

    photo = db.Column(db.Text())
    photo_type = db.Column(db.String(20))
    linkedin_url = deferred(db.Column(db.String(150)))
    uploaded_cv = deferred(db.Column(db.Boolean, default=False))

    level = relationship("Levels")
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"))

    daily_points = db.Column(db.Integer())
    total_points = db.Column(db.Integer())
    squad_points = db.Column(db.Integer())

    referral_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    course = db.Column(db.String(10))
    entry_year = db.Column(db.String())

    user = relationship("Users", cascade="all,delete")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    squad = relationship("Squads", back_populates="members", uselist=False)
    squad_id = db.Column(db.Integer, db.ForeignKey("squads.id", ondelete="SET NULL"))

    tags = relationship(
        "Tags",
        secondary="students_tags",
        secondaryjoin=sql.and_(StudentsTags.tag_id == Tags.id),
    )

    companies = relationship(
        "Companies",
        secondary="student_companies",
        secondaryjoin=sql.and_(StudentCompanies.company_id == Companies.id),
    )

    login_dates = relationship("StudentLogins")

    activities = relationship(
        "Activities",
        secondary="student_activities",
        secondaryjoin=sql.and_(StudentActivities.activity_id == Activities.id),
    )

    def is_captain(self):
        if self.squad:
            return self.user.username == self.squad.captain_ist_id
        return False

    def __repr__(self):
        return "Name: {}  |  IST Id: {}".format(self.user.name, self.user.username)
