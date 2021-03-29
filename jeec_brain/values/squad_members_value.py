from jeec_brain.values.value_composite import ValueComposite


class SquadMembersValue(ValueComposite):
	def __init__(self, members):
		super(SquadMembersValue, self).initialize({})
		members_array = []
		for member in members:
			member_value = {
				"name": member.user.name,
				"ist_id": member.user.username,
				"level": member.level.value,
				"photo": 'data: ' + member.photo_type + ';base64, ' + member.photo,
				"squad_points": member.squad_points,
				"is_captain": member.is_captain()
			}
			members_array.append(member_value)
		self.serialize_with(data=members_array)
