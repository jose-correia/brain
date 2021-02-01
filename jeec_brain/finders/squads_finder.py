from jeec_brain.models.squads import Squads
from jeec_brain.models.squad_invitations import SquadInvitations
from jeec_brain.database import db_session
from sqlalchemy import func


class SquadsFinder():

    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Squads.query.filter(Squads.name.ilike(search)).all()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Squads.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return Squads.query.order_by(Squads.name).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            squads = Squads.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return squads

    @classmethod
    def get_rank(cls, id):
        subquery = db_session.query(Squads.id, func.rank().over(
            order_by=Squads.total_points.desc()).label('rank')).subquery()

        return db_session.query(subquery).filter(subquery.c.id==id).first().rank

    @classmethod
    def get_top_10(cls):
        return Squads.query.order_by(Squads.total_points.desc()).limit(10).all()

    @classmethod
    def get_invitation_from_external_id(cls, external_id):
        return SquadInvitations.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_invitations(cls):
        return SquadInvitations.query.all()

    @classmethod
    def get_invitations_from_parameters(cls, kwargs):
        try:
            squad_invitations = SquadInvitations.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return squad_invitations