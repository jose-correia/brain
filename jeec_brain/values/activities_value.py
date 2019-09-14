from jeec_brain.values.value_composite import ValueComposite


class ActivitiesValue(ValueComposite):
	def __init__(self, activities):
		super(ActivitiesValue, self).initialize({})
		activities_array = []
		for activity in activities:
			activity_value = {
				"name": activity.name,
				"description": activity.description,
				"location": activity.location,
				"day": activity.day,
				"time": activity.time,
				"type": activity.type.name,
                "registration_open": activity.registration_open,
                "registration_link": activity.registration_link
			}
			activities_array.append(activity_value)
		self.serialize_with(data=activities_array)
