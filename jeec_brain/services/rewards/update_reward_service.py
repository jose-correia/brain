from typing import Dict, Optional
from jeec_brain.models.rewards import Rewards


class UpdateRewardService():
    
    def __init__(self, reward: Rewards, kwargs: Dict):
        self.reward = reward
        self.kwargs = kwargs

    def call(self) -> Optional[Rewards]:
        try:
            update_result = self.reward.update(**self.kwargs)
        except:
            return None
            
        return update_result
