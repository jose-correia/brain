from jeec_brain.models.activities import Activities
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.speaker_activities import SpeakerActivities
from jeec_brain.models.speakers import Speakers
from jeec_brain.models.companies import Companies


class ActivitiesFinder():

    @classmethod
    def get_from_name(cls, name):
        return Activities.query().filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Activities.query().filter_by(external_id=external_id).first()

    @classmethod
    def get_all_from_type(cls, activity_type):
        return Activities.query().filter_by(activity_type=activity_type).all()
    
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

    @classmethod
    def get_activity_speakers(cls, activity):
        return Speakers.query().join(SpeakerActivities, SpeakerActivities.speaker_id == Speakers.id).filter(SpeakerActivities.activity_id == activity.id).all()

    @classmethod
    def get_activity_companies(cls, activity):
        return Companies.query.join(CompanyActivities, CompanyActivities.company_id == Companies.id).filter(CompanyActivities.activity_id == activity.id).all()
