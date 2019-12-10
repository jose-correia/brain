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

