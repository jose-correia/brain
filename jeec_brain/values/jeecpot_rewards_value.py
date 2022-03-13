from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue


class JeecpotRewardsValue(ValueComposite):
    def __init__(self, jeecpot_rewards, student):
        super(JeecpotRewardsValue, self).initialize({})

        self.serialize_with(
            first_student_reward=RewardsValue(
                jeecpot_rewards.first_student_reward
            ).to_dict()
        )
        self.serialize_with(
            first_student_winner=student.id == jeecpot_rewards.first_student_winner_id
        )

        self.serialize_with(
            second_student_reward=RewardsValue(
                jeecpot_rewards.second_student_reward
            ).to_dict()
        )
        self.serialize_with(
            second_student_winner=student.id == jeecpot_rewards.second_student_winner_id
        )

        self.serialize_with(
            third_student_reward=RewardsValue(
                jeecpot_rewards.third_student_reward
            ).to_dict()
        )
        self.serialize_with(
            third_student_winner=student.id == jeecpot_rewards.third_student_winner_id
        )

        self.serialize_with(
            first_squad_reward=RewardsValue(
                jeecpot_rewards.first_squad_reward
            ).to_dict()
        )
        self.serialize_with(
            first_squad_winner=False
            if student.squad is None
            else student.squad.id == jeecpot_rewards.first_squad_winner_id
        )

        self.serialize_with(
            second_squad_reward=RewardsValue(
                jeecpot_rewards.second_squad_reward
            ).to_dict()
        )
        self.serialize_with(
            second_squad_winner=False
            if student.squad is None
            else student.squad.id == jeecpot_rewards.second_squad_winner_id
        )

        self.serialize_with(
            third_squad_reward=RewardsValue(
                jeecpot_rewards.third_squad_reward
            ).to_dict()
        )
        self.serialize_with(
            third_squad_winner=False
            if student.squad is None
            else student.squad.id == jeecpot_rewards.third_squad_winner_id
        )

        self.serialize_with(
            king_job_fair_reward=RewardsValue(
                jeecpot_rewards.king_job_fair_reward
            ).to_dict()
        )
        self.serialize_with(
            king_job_fair_winner=student.id == jeecpot_rewards.king_job_fair_winner_id
        )

        self.serialize_with(
            king_knowledge_reward=RewardsValue(
                jeecpot_rewards.king_knowledge_reward
            ).to_dict()
        )
        self.serialize_with(
            king_knowledge_winner=student.id == jeecpot_rewards.king_knowledge_winner_id
        )

        self.serialize_with(
            king_hacking_reward=RewardsValue(
                jeecpot_rewards.king_hacking_reward
            ).to_dict()
        )
        self.serialize_with(
            king_hacking_winner=student.id == jeecpot_rewards.king_hacking_winner_id
        )

        self.serialize_with(
            king_networking_reward=RewardsValue(
                jeecpot_rewards.king_networking_reward
            ).to_dict()
        )
        self.serialize_with(
            king_networking_winner=student.id
            == jeecpot_rewards.king_networking_winner_id
        )

        self.serialize_with(
            cv_platform_raffle_reward=RewardsValue(
                jeecpot_rewards.cv_platform_raffle_reward
            ).to_dict()
        )
        self.serialize_with(
            cv_platform_raffle_winner=student.id
            == jeecpot_rewards.cv_platform_raffle_winner_id
        )
