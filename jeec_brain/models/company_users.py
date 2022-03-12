from jeec_brain.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import sql
from jeec_brain.models.model_mixin import ModelMixin


class CompanyUsers(db.Model, ModelMixin):
    __tablename__ = "company_users"

    company = db.relationship("Companies", back_populates="users", uselist=False)
    company_id = db.Column(
        db.Integer, db.ForeignKey("companies.id", ondelete="CASCADE")
    )

    post = db.Column(db.String(50))

    food_manager = db.Column(db.Boolean, default=False)

    user = relationship("Users", cascade="all,delete")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        return "Name: {}  |  Company: {}".format(self.user.name, self.company.name)
