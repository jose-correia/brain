from jeec_brain.models.colaborators import Colaborators


class ColaboratorsFinder():

    @classmethod
    def get_from_name(cls, name):
        return Colaborators.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Colaborators.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_from_team(cls, team):
        return Colaborators.query.filter_by(team=team).all()
    
    @classmethod
    def get_all(cls):
        return Colaborators.all()
    