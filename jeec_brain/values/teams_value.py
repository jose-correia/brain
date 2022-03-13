from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.members_value import MembersValue


class TeamsValue(ValueComposite):
    def __init__(self, teams):
        super(TeamsValue, self).initialize({})
        teams_array = []
        for team in teams:
            team_value = {
                "name": team.name,
                "description": team.description,
                "members": MembersValue(team.members).to_dict(),
            }
            teams_array.append(team_value)
        self.serialize_with(data=teams_array)
