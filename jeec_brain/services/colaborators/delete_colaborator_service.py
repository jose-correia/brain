from jeec_brain.models.colaborators import Colaborators
from jeec_brain.database import db


class DeleteColaboratorService():

    def __init__(self, colaborator: Colaborators):
        self.colaborator = colaborator

    def call(self) -> bool:

        try:
            db.session.delete(self.colaborator)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
