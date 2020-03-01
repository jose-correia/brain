from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.values.activity_types_value import ActivityTypesValue
from jeec_brain.values.event_dates_value import EventDatesValue

class EventsValue(ValueComposite):
	def __init__(self, events):
		super(EventsValue, self).initialize({})
		events_array = []
		for event in events:

			event_value = {
				"name": event.name,
				"start_date": event.start_date,
				"end_date": event.end_date,
                "email": event.email,
                "location": event.location,
                "facebook_link": event.facebook_link,
                "facebook_event_link": event.facebook_event_link,
				"youtube_link": event.youtube_link,
				"instagram_link": event.instagram_link,
                "logo": EventsHandler.find_image(str(event.external_id)),
                "mobile_logo": EventsHandler.find_image(f'{event.external_id}_mobile'),
				"schedule": EventsHandler.find_image(f'{event.external_id}_schedule'),
				"blueprint": EventsHandler.find_image(f'{event.external_id}_blueprint'),
				"activity_types": ActivityTypesValue(event.activity_types.all()).to_dict(),
				"dates": EventsHandler.get_event_dates(event)
			}
			events_array.append(event_value)
		self.serialize_with(data=events_array)
