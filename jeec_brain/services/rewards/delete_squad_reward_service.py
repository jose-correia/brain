from jeec_brain.models.squads_rewards import SquadsRewards


class DeleteSquadRewardService:
    def __init__(self, squad_reward: SquadsRewards):
        self.squad_reward = squad_reward

    def call(self) -> bool:
        result = self.squad_reward.delete()
        return result
