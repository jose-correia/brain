from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.squads_handler import SquadsHandler
from jeec_brain.values.squad_members_value import SquadMembersValue


class SquadsValue(ValueComposite):
	def __init__(self, squads):
		super(SquadsValue, self).initialize({})
		squads_array = []
		for squad in squads:
			squad_value = {
				"name": squad.name,
				"daily_points": squad.daily_points,
				"total_points": squad.total_points,
				"image": SquadsHandler.find_squad_image(squad.name),
                "members": SquadMembersValue(squad.members).to_dict()
			}
			squads_array.append(squad_value)
		self.serialize_with(data=squads_array)
