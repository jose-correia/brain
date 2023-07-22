from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue


class MultiplayerPrizesValue(ValueComposite):
    def __init__(self, jeecpot_rewards, daily_squad_reward):
        super(MultiplayerPrizesValue, self).initialize({})

        self.serialize_with(
            top_squads=RewardsValue(jeecpot_rewards.first_squad_reward).to_dict()
        )
        self.serialize_with(daily_squad=RewardsValue(daily_squad_reward).to_dict())
