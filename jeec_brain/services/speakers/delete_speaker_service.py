from jeec_brain.models.speakers import Speakers
from jeec_brain.database import db


class DeleteSpeakerService():

    def __init__(self, speaker: Speakers):
        self.speaker = speaker

    def call(self) -> bool:

        try:
            db.session.delete(self.speaker)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
