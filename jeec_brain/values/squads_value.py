from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.squads_handler import SquadsHandler
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.values.squad_members_value import SquadMembersValue


class SquadsValue(ValueComposite):
    def __init__(self, squads):
        super(SquadsValue, self).initialize({})

        if not isinstance(squads, list):
            squads = [squads]

        squads_array = []
        for squad in squads:
            squad_value = {
                "name": squad.name,
                "cry": squad.cry,
                "daily_points": squad.daily_points,
                "total_points": squad.total_points,
                "image": SquadsHandler.find_squad_image(str(squad.external_id)),
                "members": SquadMembersValue(squad.members).to_dict(),
                "captain_ist_id": squad.captain_ist_id,
                "rank": SquadsFinder.get_rank(squad.id),
            }
            squads_array.append(squad_value)

        if len(squads_array) == 1:
            self.serialize_with(data=squads_array[0])
        else:
            self.serialize_with(data=squads_array)
