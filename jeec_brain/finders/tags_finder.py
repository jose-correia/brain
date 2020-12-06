from jeec_brain.models.tags import Tags
from jeec_brain.models.students_tags import StudentsTags
from jeec_brain.models.activities_tags import ActivitiesTags
from jeec_brain.models.activities import Activities

class TagsFinder():

    @classmethod
    def get_from_external_id(cls, external_id):
        return Tags.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return Tags.query.order_by(Tags.name).all()

    @classmethod
    def get_by_name(cls, name):
        return Tags.query.filter_by(name=name).first()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            return Tags.query.filter_by(**kwargs).all()
        except Exception:
            return None

    @classmethod
    def get_student_tag(cls, student, tag):
        return StudentsTags.query.filter_by(student_id=student.id, tag_id=tag.id).first()

    @classmethod
    def get_activity_tags_from_activity_id(cls, external_id):
        return ActivitiesTags.query.join(Activities, Activities.id == ActivitiesTags.activity_id).filter(Activities.external_id == external_id).all()