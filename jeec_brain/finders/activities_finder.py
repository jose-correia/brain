from jeec_brain.models.activities import Activities
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.speaker_activities import SpeakerActivities
from jeec_brain.models.activities_tags import ActivitiesTags
from jeec_brain.models.speakers import Speakers
from jeec_brain.models.companies import Companies
from jeec_brain.models.tags import Tags
from jeec_brain.models.events import Events
from jeec_brain.finders.events_finder import EventsFinder
from datetime import datetime, timedelta

class ActivitiesFinder():

    @classmethod
    def get_from_name(cls, name):
        return Activities.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Activities.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_all_from_type(cls, activity_type):
        return Activities.query.filter_by(activity_type=activity_type).order_by(Activities.day, Activities.time).all()
    
    @classmethod
    def get_all_from_type_and_event(cls, activity_type, event=None):
        if(event is None):
            event = EventsFinder.get_default_event()
            
        return Activities.query.filter_by(activity_type=activity_type, event_id=event.id).order_by(Activities.day, Activities.time).all()
    
    @classmethod
    def get_all(cls):
        return Activities.query.order_by(Activities.day, Activities.time, Activities.activity_type_id).all()

    @classmethod
    def get_quests(cls):
        now = datetime.utcnow().strftime('%d %b %Y, %a')

        return Activities.query.filter(Activities.quest == True).filter(Activities.day == now).order_by(Activities.day, Activities.time, Activities.activity_type_id).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            return Activities.query.filter_by(**kwargs).order_by(Activities.activity_type_id, Activities.day, Activities.time).all()
        except Exception:
            return None

    @classmethod
    def search_by_name_and_event(cls, name, event=None):
        search = "%{}%".format(name)

        if(event is None):
            event = EventsFinder.get_default_event()

        return Activities.query.filter(Activities.name.ilike(search) & (Activities.event_id == event.id)).order_by(Activities.day, Activities.time, Activities.activity_type_id).all()
    
    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)

        return Activities.query.filter(Activities.name.ilike(search)).order_by(Activities.day, Activities.time, Activities.activity_type_id).all()
    
    @classmethod
    def get_company_activities_from_activity_id(cls, external_id):
        return CompanyActivities.query.join(Activities, Activities.id == CompanyActivities.activity_id).filter(Activities.external_id == external_id).all()
    
    @classmethod
    def get_speaker_activities_from_activity_id(cls, external_id):
        return SpeakerActivities.query.join(Activities, Activities.id == SpeakerActivities.activity_id).filter(Activities.external_id == external_id).all()

    @classmethod
    def get_activity_speakers(cls, activity):
        return Speakers.query.join(SpeakerActivities, SpeakerActivities.speaker_id == Speakers.id).filter(SpeakerActivities.activity_id == activity.id).order_by(Speakers.name).all()

    @classmethod
    def get_activity_companies(cls, activity):
        return Companies.query.join(CompanyActivities, CompanyActivities.company_id == Companies.id).filter(CompanyActivities.activity_id == activity.id).order_by(Companies.name).all()

    @classmethod
    def get_activity_tags(cls, activity):
        return Tags.query.join(ActivitiesTags, ActivitiesTags.tag_id == Tags.id).filter(ActivitiesTags.activity_id == activity.id).order_by(Tags.name).all()

    @classmethod
    def get_next_company_activity(cls, company):
        now = datetime.utcnow() - timedelta(minutes=5)
        day = now.strftime('%d %b %Y, %a')
        time = now.strftime("%H:%M")

        return Activities.query.join(CompanyActivities, Activities.id == CompanyActivities.activity_id).filter((CompanyActivities.company_id == company.id) & (Activities.day == day) & (Activities.time <= time) & (Activities.end_time > time)).first()

    @classmethod
    def get_activities_from_speaker_and_event(cls, speaker, event):
        return Activities.query.filter((Events.id == event.id) & (Events.id == Activities.event_id) & (SpeakerActivities.activity_id == Activities.id) & (SpeakerActivities.speaker_id == speaker.id)).all()

    @classmethod
    def get_activities_from_company_and_event(cls, company, event):
        return Activities.query.filter((Events.id == event.id) & (Events.id == Activities.event_id) & (CompanyActivities.activity_id == Activities.id) & (CompanyActivities.company_id == company.id)).all()

    @classmethod
    def get_next_activity(cls):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        activity = Activities.query.filter(Activities.time >= current_time).order_by(Activities.time).first()

        if activity:
            return Activities.query.filter(Activities.time == activity.time).all()
        else:
            return []