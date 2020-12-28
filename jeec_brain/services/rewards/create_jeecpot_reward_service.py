import logging
from jeec_brain.models.jeecpot_rewards import JeecpotRewards
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateJeecpotRewardService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[JeecpotRewards]:
        
        jeecpot_reward = JeecpotRewards.create(**self.kwargs)

        if not jeecpot_reward:
            return None

        return jeecpot_reward

