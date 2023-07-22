from jeec_brain.models.events import Events


class DeleteEventService:
    def __init__(self, event: Events):
        self.event = event

    def call(self) -> bool:
        result = self.event.delete()
        return result
