from jeec_brain.values.value_composite import ValueComposite


class ActivityValue(ValueComposite):
    def __init__(self, activity):
        super(ActivityValue, self).initialize({})
        self.serialize_with(name=activity.name)
        
        self.serialize_with(description=activity.description)
        self.serialize_with(location=activity.location)
        self.serialize_with(datetime=str(activity.datetime))
        self.serialize_with(type=activity.type)
  
        self.serialize_with(company_external_id=activity.company.external_id)
        
        self.serialize_with(registration_open=activity.registration_open)

        if activity.registration_open:
            self.serialize_with(registration_link=activity.registration_link)
