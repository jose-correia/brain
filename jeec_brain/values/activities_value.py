from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.speakers_value import SpeakersValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.values.rewards_value import RewardsValue

class ActivitiesValue(ValueComposite):
	def __init__(self, activities):
		super(ActivitiesValue, self).initialize({})
		activities_array = []
		for activity in activities:
			
			activity_speakers = ActivitiesFinder.get_activity_speakers(activity)
			activity_companies = ActivitiesFinder.get_activity_companies(activity)

			activity_value = {
				"name": activity.name,
				"description": activity.description,
				"location": activity.location,
				"day": activity.day,
				"time": activity.time,
				"end_time": activity.end_time,
				"type": activity.activity_type.name,
                "registration_open": activity.registration_open,
                "registration_link": activity.registration_link,
				"zoom_link": activity.zoom_link,
				"speakers": SpeakersValue(activity_speakers).to_dict(),
				"moderator": activity.moderator.name if activity.moderator else "",
				"reward": RewardsValue(activity.reward).to_dict(),
				"companies": CompaniesValue(activity_companies, True).to_dict()
			}
			activities_array.append(activity_value)
		self.serialize_with(data=activities_array)
