from jeec_brain.values.value_composite import ValueComposite


class StudentActivityTypesValue(ValueComposite):
	def __init__(self, activity_types):
		super(StudentActivityTypesValue, self).initialize({})
		activity_types_array = []
		for activity_type in activity_types:
			activity_type_value = {
				"name": activity_type.name,
				"description": activity_type.description
			}
			activity_types_array.append(activity_type_value)
		self.serialize_with(data=activity_types_array)
