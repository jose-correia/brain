from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.values.rewards_value import RewardsValue

class LevelsValue(ValueComposite):
	def __init__(self, levels, details=False):
		super(LevelsValue, self).initialize({})

		if (not isinstance(levels, list)):
			levels = [levels]
			
		levels_array = []
		for level in levels:
			if level is not None:
				level_value = {
				"value": level.value,
				"end_points": level.points + 1,
				"start_points": 0 if level.value == 1 else LevelsFinder.get_level_by_value(level.value - 1).points + 1
				}
				
				if(details and level.reward is not None):
					level_value['reward'] = RewardsValue(level.reward).to_dict()

			else:
				level_value = {
				"value": 0,
				"end_points": 0,
				"start_points": 0
				}

			levels_array.append(level_value)

		if(len(levels_array) == 1):
			self.serialize_with(data=levels_array[0])
		else:
			self.serialize_with(data=levels_array)