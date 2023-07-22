from jeec_brain.values.value_composite import ValueComposite


class StudentEventInfoValue(ValueComposite):
    def __init__(self, event):
        super(StudentEventInfoValue, self).initialize({})
        activity_types_array = []
        for activity_type in event.activity_types:
            activity_type_value = {
                "name": activity_type.name,
                "description": activity_type.description,
            }
            activity_types_array.append(activity_type_value)
        self.serialize_with(activity_types=activity_types_array)
        self.serialize_with(facebook_link=event.facebook_link)
        self.serialize_with(instagram_link=event.instagram_link)
