from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.speakers_value import SpeakersValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.finders.activities_finder import ActivitiesFinder


class StudentActivitiesValue(ValueComposite):
	def __init__(self, event, activities, student):
		super(StudentActivitiesValue, self).initialize({})
		activities_array = []
		for activity in activities:
			if(not activity.activity_type.show_in_app):
				continue

			activity_speakers = ActivitiesFinder.get_activity_speakers(activity)
			activity_companies = ActivitiesFinder.get_activity_companies(activity)
			activity_tags = ActivitiesFinder.get_activity_tags(activity)

			activity_value = {
				"name": activity.name,
				"description": activity.description,
				"location": activity.location,
				"day": activity.day,
				"time": activity.time,
				"end_time": activity.end_time,
				"type": activity.activity_type.name,
				"points": activity.points,
				"quest": activity.quest,
                "registration_open": activity.registration_open,
                "registration_link": activity.registration_link,
				"speakers": SpeakersValue(activity_speakers).to_dict(),
				"companies": CompaniesValue(activity_companies, True).to_dict(),
				"participated": activity in student.activities,
				"zoom_url": activity.zoom_link,
				"interest": not set(activity_tags).isdisjoint(student.tags) or not set(activity_companies).isdisjoint(student.companies)
			}
			activities_array.append(activity_value)
		self.serialize_with(data=activities_array)
		self.serialize_with(start_date=event.start_date)
		self.serialize_with(end_date=event.end_date)