from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.handlers.squads_handler import SquadsHandler

class SquadInvitationsValue(ValueComposite):
	def __init__(self, invitations):
		super(SquadInvitationsValue, self).initialize({})
		invitations_array = []
		for invitation in invitations:
			sender = StudentsFinder.get_from_id(invitation.sender_id)
			squad = sender.squad

			invitation_value = {
				"external_id": invitation.external_id,
				"squad_name": squad.name,
				"squad_cry": squad.cry,
				"squad_rank": SquadsFinder.get_rank(squad.id),
				"squad_image": SquadsHandler.find_squad_image(str(squad.external_id)),
				"sender_name": sender.name
			}
			invitations_array.append(invitation_value)
		self.serialize_with(data=invitations_array)
