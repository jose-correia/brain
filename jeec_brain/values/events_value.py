from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.values.activity_types_value import ActivityTypesValue
from jeec_brain.values.event_dates_value import EventDatesValue
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder

class EventsValue(ValueComposite):
	def __init__(self, events):
		super(EventsValue, self).initialize({})

		if (not isinstance(events, list)): 
			events = [events]

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
				"activity_types": ActivityTypesValue(ActivityTypesFinder.get_from_parameters({'event_id':event.id, 'show_in_schedule':True})).to_dict(),
				"dates": EventsHandler.get_event_dates(event),
				"show_schedule": event.show_schedule,
				"show_registrations": event.show_registrations
			}
			events_array.append(event_value)
		self.serialize_with(data=events_array)

		if(len(events_array) == 1):
			self.serialize_with(data=events_array[0])
		else:
			self.serialize_with(data=events_array)
