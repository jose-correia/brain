import logging
from jeec_brain.models.rewards import Rewards
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateRewardService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Rewards]:

        reward = Rewards.create(**self.kwargs)

        if not reward:
            return None

        return reward
