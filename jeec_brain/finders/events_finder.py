from jeec_brain.models.events import Events

class EventsFinder():

    @classmethod
    def get_from_name(cls, name):
        return Events.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Events.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
            return Events.query.order_by(Events.updated_at).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            events = Events.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return events

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Events.query.filter(Events.name.ilike(search)).all()
    
    @classmethod
    def get_default_event(cls):
        return Events.query.filter_by(default=True).first()
    