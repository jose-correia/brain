from jeec_brain.models.speakers import Speakers
from jeec_brain.models.speaker_activities import SpeakerActivities
from jeec_brain.models.activities import Activities
from jeec_brain.models.events import Events

class SpeakersFinder():

    @classmethod
    def get_from_name(cls, name):
        return Speakers.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Speakers.query.filter_by(external_id=external_id).first()

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Speakers.query.filter(Speakers.name.ilike(search)).order_by(Speakers.name).all()

    @classmethod
    def get_from_activity(cls, activity):
        return Speakers.query.filter(Speakers.id == SpeakerActivities.speaker_id, SpeakerActivities.activity_id == activity.id).all()
    
    @classmethod
    def get_all(cls):
        return Speakers.query.order_by(Speakers.name).all()
    
    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            speakers = Speakers.query.filter_by(**kwargs).order_by(Speakers.name).all()
        except Exception:
            return None
        
        return speakers

    @classmethod
    def get_website_speakers(cls, event, kwargs={}):
        return Speakers.query.filter((Speakers.id == SpeakerActivities.speaker_id) & (Activities.id == SpeakerActivities.activity_id) & (Activities.event_id == Events.id) & (Events.id == event.id)).filter_by(**kwargs).all()
