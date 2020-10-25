from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompaniesTags(db.Model, ModelMixin):
    __tablename__ = 'companies_tags'

    tag_id = Column(Integer, ForeignKey('speakers.id'), index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), index=True)