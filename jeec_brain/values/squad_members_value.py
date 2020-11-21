from jeec_brain.values.value_composite import ValueComposite


class SquadMembersValue(ValueComposite):
	def __init__(self, members):
		super(SquadMembersValue, self).initialize({})
		members_array = []
		for member in members:
			member_value = {
				"name": member.name,
				"ist_id": member.ist_id,
				"level": member.level.value,
				"photo": member.photo,
				"photo_type": member.photo_type,
				"squad_points": member.squad_points,
				"is_captain": member.ist_id == member.squad.captain_ist_id
			}
			members_array.append(member_value)
		self.serialize_with(data=members_array)
