from jeec_brain.models.teams import Teams


class TeamsFinder():

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Teams.query.filter(Teams.name.ilike(search)).all()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Teams.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return Teams.query.order_by(Teams.name).all()

    @classmethod
    def get_from_event_id(cls, event_id):
        return Teams.query.filter_by(event_id=event_id)

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            teams = Teams.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return teams