from jeec_brain.models.students import Students
from jeec_brain.database import db


class DeleteStudentService():

    def __init__(self, student: Students):
        self.student = student

    def call(self) -> bool:

        try:
            db.session.delete(self.student)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
