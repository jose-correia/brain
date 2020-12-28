from jeec_brain.models.rewards import Rewards
from jeec_brain.models.squads_rewards import SquadsRewards
from jeec_brain.models.jeecpot_rewards import JeecpotRewards

class RewardsFinder():

    @classmethod
    def get_reward_from_external_id(cls, external_id):
        return Rewards.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_rewards(cls):
        return Rewards.all()

    @classmethod
    def get_rewards_from_parameters(cls, kwargs):
        try:
            return Rewards.query.filter_by(**kwargs).all()
        except Exception:
            return None

    @classmethod
    def get_rewards_from_search(cls, search):
        search = "%{}%".format(search)
        return Rewards.query.filter(Rewards.name.ilike(search)).all()

    @classmethod
    def get_squad_reward_from_external_id(cls, external_id):
        return SquadsRewards.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_squad_rewards(cls):
        return SquadsRewards.query.order_by(SquadsRewards.date).all()

    @classmethod
    def get_squad_rewards_from_parameters(cls, kwargs):
        try:
            return SquadsRewards.query.filter_by(**kwargs).all()
        except Exception:
            return None

    @classmethod
    def get_squad_reward_from_date(cls, date):
        return SquadsRewards.query.filter_by(date=date).first()

    @classmethod
    def get_jeecpot_reward_from_external_id(cls, external_id):
        return JeecpotRewards.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_jeecpot_rewards(cls):
        return JeecpotRewards.all()

    @classmethod
    def get_jeecpot_rewards_from_parameters(cls, kwargs):
        try:
            return JeecpotRewards.query.filter_by(**kwargs).all()
        except Exception:
            return None