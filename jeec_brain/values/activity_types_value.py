from jeec_brain.values.value_composite import ValueComposite


class ActivityTypesValue(ValueComposite):
    def __init__(self, activity_types):
        super(ActivityTypesValue, self).initialize({})
        activity_types_array = []
        for activity_type in activity_types:
            activity_type_value = {
                "name": activity_type.name,
                "show_in_home": activity_type.show_in_home,
                "show_in_schedule": activity_type.show_in_schedule,
            }
            activity_types_array.append(activity_type_value)
        self.serialize_with(data=activity_types_array)
