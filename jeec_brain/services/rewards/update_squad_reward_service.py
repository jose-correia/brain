from typing import Dict, Optional
from jeec_brain.models.squads_rewards import SquadsRewards


class UpdateSquadRewardService():
    
    def __init__(self, squad_reward: SquadsRewards, kwargs: Dict):
        self.squad_reward = squad_reward
        self.kwargs = kwargs

    def call(self) -> Optional[SquadsRewards]:
        try:
            update_result = self.squad_reward.update(**self.kwargs)
        except:
            return None
            
        return update_result
