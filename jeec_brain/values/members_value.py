from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.teams_handler import TeamsHandler


class MembersValue(ValueComposite):
    def __init__(self, members):
        super(MembersValue, self).initialize({})
        members_array = []
        for member in members:
            member_value = {
                "name": member.name,
                "linkedin_url": member.linkedin_url,
                "image": TeamsHandler.find_member_image(member.name),
            }
            members_array.append(member_value)
        self.serialize_with(data=members_array)
