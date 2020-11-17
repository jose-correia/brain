from jeec_brain.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import sql
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.companies import Companies
from jeec_brain.models.squads import Squads
from jeec_brain.models.tags import Tags
from jeec_brain.models.students_tags import StudentsTags
from jeec_brain.models.companies import Companies
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.rewards import Rewards
from jeec_brain.models.students_rewards import StudentsRewards
from jeec_brain.models.activities import Activities
from jeec_brain.models.student_activities import StudentActivities
from jeec_brain.models.levels import Levels


class Students(ModelMixin, db.Model):
    __tablename__ = 'students'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    ist_id = db.Column(db.String(10), unique=True, nullable=False)
    photo = db.Column(db.Text())
    photo_type = db.Column(db.String(20))
    fenix_auth_code = db.Column(db.Text())
    linkedin_url = db.Column(db.String(150))
    uploaded_cv = db.Column(db.Boolean, default=False)

    level = relationship('Levels')
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))

    daily_points = db.Column(db.Integer())
    total_points = db.Column(db.Integer())
    squad_points = db.Column(db.Integer())

    user = relationship('Users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    stared_companies = relationship("Companies",
                                         secondary="student_companies",
                                         secondaryjoin=sql.and_(StudentCompanies.company_id == Companies.id))

    squad = relationship('Squads', back_populates="members", uselist=False)
    squad_id = db.Column(db.Integer, db.ForeignKey('squads.id', ondelete='SET NULL'))

    tags = relationship("Tags",
        secondary="students_tags",
        secondaryjoin=sql.and_(StudentsTags.tag_id == Tags.id))

    companies = relationship("Companies",
        secondary="student_companies",
        secondaryjoin=sql.and_(StudentCompanies.company_id == Companies.id))

    rewards = relationship("Rewards",
        secondary="students_rewards",
        secondaryjoin=sql.and_(StudentsRewards.reward_id == Rewards.id))

    activities = relationship("Activities",
        secondary="student_activities",
        secondaryjoin=sql.and_(StudentActivities.student_id == Activities.id))

    def __repr__(self):
        return 'Email:: {}  |  Name: {}'.format(self.name, self.ist_id)

    # def accept_terms(self):
    #     self.accept_terms = True
