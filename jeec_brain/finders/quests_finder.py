from jeec_brain.models.quests import Quests

class QuestsFinder:
    @classmethod
    def get_quest_from_external_id(cls, external_id):
        return Quests.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_all(cls):
        return Quests.query.order_by(Quests.id).all()

    @classmethod
    def get_quest_by_id(cls, id):
        return Quests.query.filter_by(id=id).first()

    @classmethod
    def get_quest_by_reward_id(cls,reward_id):
        return Quests.query.filter_by(reward_id=reward_id).all()
    
    @classmethod
    def get_quest_by_name(cls,name):
        search = "%{}%".format(name)
        return (
            Quests.query.filter(Quests.name.ilike(search))
            .order_by(Quests.id)
            .all())
   

