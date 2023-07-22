from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Tags(db.Model, ModelMixin):
    __tablename__ = "tags"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "Name: {}".format(self.name)
