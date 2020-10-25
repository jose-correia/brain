from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class StudentsTags(db.Model, ModelMixin):
    __tablename__ = 'students_tags'

    tag_id = Column(Integer, ForeignKey('speakers.id'), index=True)
    student_id = Column(Integer, ForeignKey('students.id'), index=True)