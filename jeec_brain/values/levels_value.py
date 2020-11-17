from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.finders.levels_finder import LevelsFinder

class LevelsValue(ValueComposite):
	def __init__(self, level):
		super(LevelsValue, self).initialize({})
	
		self.serialize_with(value=level.value)
		self.serialize_with(end_points=level.points)

		if(level.value == 0):
			self.serialize_with(start_points=0)
		else:
			self.serialize_with(start_points=LevelsFinder.get_level_by_value(level.value - 1).points)