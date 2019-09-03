from jeec_brain.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import sql
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.companies import Companies


class Students(ModelMixin, db.Model):
    __tablename__ = 'students'
    
    name = db.Column(db.String(100))
    ist_id = db.Column(db.String(10), unique=True, nullable=False)

    user = relationship('Users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    accepted_terms = db.Column(db.Boolean, default=False)

    stared_companies = relationship("Companies",
                                         secondary="student_companies",
                                         secondaryjoin=sql.and_(StudentCompanies.company_id == Companies.id))

    def __repr__(self):
        return 'Email:: {}  |  Name: {}'.format(self.name, self.ist_id)

    def accept_terms(self):
        self.accept_terms = True
