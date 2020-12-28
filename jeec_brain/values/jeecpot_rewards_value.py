from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue

class JeecpotRewardsValue(ValueComposite):
	def __init__(self, jeecpot_rewards, student):
		super(JeecpotRewardsValue, self).initialize({})

		self.serialize_with(student_reward=RewardsValue(jeecpot_rewards.student_reward).to_dict())
		self.serialize_with(student_winner=student.id == jeecpot_rewards.student_winner_id)
		
		self.serialize_with(first_squad_reward=RewardsValue(jeecpot_rewards.first_squad_reward).to_dict())
		self.serialize_with(first_squad_winner=None if student.squad is None else student.squad.id == jeecpot_rewards.first_squad_winner_id)

		self.serialize_with(second_squad_reward=RewardsValue(jeecpot_rewards.second_squad_reward).to_dict())
		self.serialize_with(second_squad_winner=None if student.squad is None else student.squad.id == jeecpot_rewards.second_squad_winner_id)

		self.serialize_with(third_squad_reward=RewardsValue(jeecpot_rewards.third_squad_reward).to_dict())
		self.serialize_with(third_squad_winner=None if student.squad is None else student.squad.id == jeecpot_rewards.third_squad_winner_id)