from jeec_brain.values.multiplayer_rewards_value import MultiplayerPrizesValue
from jeec_brain.values.singleplayer_rewards_value import SingleplayerPrizesValue
from jeec_brain.values.value_composite import ValueComposite


class WebsiteRewardsValue(ValueComposite):
    def __init__(
        self, jeecpot_rewards, level_reward, activity_reward, daily_squad_reward
    ):
        super(WebsiteRewardsValue, self).initialize({})

        self.serialize_with(
            singleplayer=SingleplayerPrizesValue(
                jeecpot_rewards, level_reward, activity_reward
            ).to_dict()
        )
        self.serialize_with(
            multiplayer=MultiplayerPrizesValue(
                jeecpot_rewards, daily_squad_reward
            ).to_dict()
        )
