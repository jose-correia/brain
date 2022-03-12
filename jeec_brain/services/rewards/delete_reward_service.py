from jeec_brain.models.rewards import Rewards


class DeleteRewardService:
    def __init__(self, reward: Rewards):
        self.reward = reward

    def call(self) -> bool:
        result = self.reward.delete()
        return result
