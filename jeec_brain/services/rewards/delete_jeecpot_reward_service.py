from jeec_brain.models.jeecpot_rewards import JeecpotRewards


class DeleteJeecpotRewardService:
    def __init__(self, jeecpot_reward: JeecpotRewards):
        self.jeecpot_reward = jeecpot_reward

    def call(self) -> bool:
        result = self.jeecpot_reward.delete()
        return result
