from typing import Dict, Optional
from jeec_brain.models.jeecpot_rewards import JeecpotRewards


class UpdateJeecpotRewardService:
    def __init__(self, jeecpot_reward: JeecpotRewards, kwargs: Dict):
        self.jeecpot_reward = jeecpot_reward
        self.kwargs = kwargs

    def call(self) -> Optional[JeecpotRewards]:
        try:
            update_result = self.jeecpot_reward.update(**self.kwargs)
        except:
            return None

        return update_result
