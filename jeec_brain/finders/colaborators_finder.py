from jeec_brain.models.colaborators import Colaborators
from jeec_brain.models.teams import Teams

class ColaboratorsFinder():

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Colaborators.query.filter(Colaborators.name.ilike(search)).all()
    
    @classmethod
    def get_from_external_id(cls, external_id):
        return Colaborators.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_from_team(cls, team):
        return Colaborators.query.filter_by(team=team).all()

    @classmethod
    def get_from_event_and_name(cls, event_id, name):
        return Colaborators.query.filter((Colaborators.name == name) & (Teams.id == Colaborators.team_id) & (Teams.event_id == event_id))
    
    @classmethod
    def get_all(cls):
        return Colaborators.query.order_by(Colaborators.name)
    