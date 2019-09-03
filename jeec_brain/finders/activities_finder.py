from jeec_brain.models.activities import Activities
from jeec_brain.models.enums.activity_type_enum import ActivityTypeEnum


class ActivitiesFinder():

    @classmethod
    def get_from_name(cls, name):
        return Activities.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Activities.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_from_location(cls, location):
        return Activities.query.filter_by(location=location).all()
    
    @classmethod
    def get_all_job_fair(cls):
        return Activities.query.filter_by(type=ActivityTypeEnum.job_fair).all()
    
    @classmethod
    def get_all_workshops(cls):
        return Activities.query.filter_by(type=ActivityTypeEnum.workshop).all()
    
    @classmethod
    def get_all_presentations(cls):
        return Activities.query.filter_by(type=ActivityTypeEnum.presentation).all()
    
    @classmethod
    def get_all_tech_talks(cls):
        return Activities.query.filter_by(type=ActivityTypeEnum.tech_talk).all()
    
    @classmethod
    def get_all_matchmaking(cls):
        return Activities.query.filter_by(type=ActivityTypeEnum.matchmaking).all()
    
    @classmethod
    def get_all(cls):
        return Activities.all()

    @classmethod
    def get_all_type_date(cls, activity_type, date):
        return Activities.query.filter_by(type=activity_type, datetime=date).all()
    