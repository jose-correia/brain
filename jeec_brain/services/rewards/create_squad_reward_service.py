import logging
from jeec_brain.models.squads_rewards import SquadsRewards
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSquadRewardService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[SquadsRewards]:
        
        squad_reward = SquadsRewards.create(**self.kwargs)

        if not squad_reward:
            return None

        return squad_reward

