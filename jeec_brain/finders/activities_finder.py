from jeec_brain.models.activities import Activities
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.speaker_activities import SpeakerActivities
from jeec_brain.models.enums.activity_type_enum import ActivityTypeEnum


class ActivitiesFinder():

    @classmethod
    def get_from_name(cls, name):
        return Activities.query().filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Activities.query().filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return Activities.query().order_by(Activities.updated_at).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            return Activities.query().filter_by(**kwargs).all()
        except Exception:
            return None
        

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Activities.query().filter(Activities.name.ilike(search)).all()
    
    @classmethod
    def get_company_activities_from_activity_id(cls, external_id):
        return CompanyActivities.query.join(Activities, Activities.id == CompanyActivities.activity_id).filter(Activities.external_id == external_id).all()
    
    @classmethod
    def get_speaker_activities_from_activity_id(cls, external_id):
        return SpeakerActivities.query.join(Activities, Activities.id == SpeakerActivities.activity_id).filter(Activities.external_id == external_id).all()
