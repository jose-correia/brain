from flask import current_app
# SERVICES
from jeec_brain.services.events.create_event_service import CreateEventService
from jeec_brain.services.events.update_event_service import UpdateEventService
from jeec_brain.services.events.delete_event_service import DeleteEventService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from datetime import datetime, timedelta

class EventsHandler():

    @classmethod
    def create_event(cls, **kwargs):
        return CreateEventService(kwargs=kwargs).call()

    @classmethod
    def update_event(cls, event, **kwargs):
        return UpdateEventService(event=event, kwargs=kwargs).call()

    @classmethod
    def delete_event(cls, event):
        event_name = event.name

        if DeleteEventService(event=event).call():
            for extension in current_app.config['ALLOWED_IMAGES']:
                event_name = event_name.lower().replace(' ', '_')

                filename = f'{event_name}.{extension}'
                DeleteImageService(filename, 'static/events/images').call()

                filename = f'{event_name}_mobile.{extension}'
                DeleteImageService(filename, 'static/events/images').call()

                filename = f'{event_name}_blueprint.{extension}'
                DeleteImageService(filename, 'static/events/images').call()

                filename = f'{event_name}_schedule.{extension}'
                DeleteImageService(filename, 'static/events/images').call()
            
            return DeleteEventService(event)
        return False

    @classmethod
    def upload_image(cls, file, image_name):
        return UploadImageService(file, image_name, 'static/events/images').call()

    @classmethod
    def find_image(cls, image_name):
        return FindImageService(image_name, 'static/events/images').call()

    @classmethod
    def get_event_dates(cls, event):
        event_dates = []
        start_date = datetime.strptime(event.start_date, '%d %b %Y, %a')
        end_date = datetime.strptime(event.end_date, '%d %b %Y, %a')

        date = start_date

        while date <= end_date:
            event_dates.append(date.strftime('%d %b %Y, %a'))
            date = date + timedelta(days=1)
            
        return event_dates
