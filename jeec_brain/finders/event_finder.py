from jeec_brain.models.event import Event


class EventFidner():

    @classmethod
    def get_event(cls):
        return Event.query().first()
        

