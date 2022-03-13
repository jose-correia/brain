from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue


class SingleplayerPrizesValue(ValueComposite):
    def __init__(self, jeecpot_rewards, level_reward, activity_reward):
        super(SingleplayerPrizesValue, self).initialize({})

        self.serialize_with(
            top_participants=RewardsValue(
                jeecpot_rewards.first_student_reward
            ).to_dict()
        )
        self.serialize_with(
            king_job_fair=RewardsValue(jeecpot_rewards.king_job_fair_reward).to_dict()
        )
        self.serialize_with(
            king_knowledge=RewardsValue(jeecpot_rewards.king_knowledge_reward).to_dict()
        )
        self.serialize_with(
            king_hacking=RewardsValue(jeecpot_rewards.king_hacking_reward).to_dict()
        )
        self.serialize_with(
            king_networking=RewardsValue(
                jeecpot_rewards.king_networking_reward
            ).to_dict()
        )
        self.serialize_with(
            cv_platform_raffle=RewardsValue(
                jeecpot_rewards.cv_platform_raffle_reward
            ).to_dict()
        )
        self.serialize_with(progress_bar=RewardsValue(level_reward).to_dict())
        self.serialize_with(activity_raffle=RewardsValue(activity_reward).to_dict())
