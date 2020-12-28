from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.rewards_value import RewardsValue
from jeec_brain.finders.squads_finder import SquadsFinder

class SquadsRewardsValue(ValueComposite):
	def __init__(self, squads_rewards, squad):
		super(SquadsRewardsValue, self).initialize({})

		squads_rewards_array = []
		for squad_reward in squads_rewards:
			squad_reward_value = {
				"reward": RewardsValue(squad_reward.reward).to_dict(),
				"date": squad_reward.date,
				"winner": False if squad is None else squad.id == squad_reward.winner_id
			}
				
			squads_rewards_array.append(squad_reward_value)

		self.serialize_with(data=squads_rewards_array)