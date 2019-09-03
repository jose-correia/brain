from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.activity_value import ActivityValue


class SpeakerValue(ValueComposite):
    def __init__(self, speaker, details=False):
        super(SpeakerValue, self).initialize({})
        self.serialize_with(name=speaker.name)
        self.serialize_with(company=speaker.company)
        self.serialize_with(position=speaker.position)
        self.serialize_with(country=speaker.country)

        if details:
            activities_array = []
            for activity in speaker.activities:
                activities_array.append({
                    "activity": ActivityValue(activity).to_dict(),
                })

            self.serialize_with(activities=activities_array)
            self.serialize_with(bio=speaker.bio)
