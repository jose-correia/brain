from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.rewards_handler import RewardsHandler


class RewardsValue(ValueComposite):
    def __init__(self, reward):
        super(RewardsValue, self).initialize({})

        if reward is not None:
            self.serialize_with(name=reward.name)
            self.serialize_with(
                image=RewardsHandler.find_reward_image(str(reward.external_id))
            )
        else:
            self.serialize_with(name="")
            self.serialize_with(image="")
