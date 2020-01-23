import logging
from jeec_brain.models.students import Students
from typing import Optional

logger = logging.getLogger(__name__)


class CreateStudentService():

    def __init__(self, name, ist_id, user_id):
        self.name = name
        self.ist_id = ist_id
        self.user_id = user_id

    def call(self) -> Optional[Students]:
        
        student = Students.create(
            name=self.name,
            ist_id=self.ist_id,
            user_id=self.user_id
        )

        if not student:
            return None

        return student

