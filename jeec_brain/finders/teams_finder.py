from jeec_brain.models.teams import Teams


class TeamsFinder():

    @classmethod
    def get_from_name(cls, name):
        return Teams.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Teams.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return Teams.all()
    