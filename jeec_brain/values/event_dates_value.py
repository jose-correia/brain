from jeec_brain.values.value_composite import ValueComposite


class EventDatesValue(ValueComposite):
    def __init__(self, event_dates):
        super(EventDatesValue, self).initialize({})
        event_dates_array = []
        for event_date in event_dates:
            event_date_value = {"day": event_date}
            event_dates_array.append(event_date_value)
        self.serialize_with(data=event_dates_array)
