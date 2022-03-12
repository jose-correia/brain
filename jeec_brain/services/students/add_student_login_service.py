from typing import Optional
from jeec_brain.models.student_logins import StudentLogins


class AddStudentLoginService(object):
    def __init__(self, student_id, date):
        self.student_id = student_id
        self.date = date

    def call(self) -> Optional[StudentLogins]:
        student_login = StudentLogins.create(student_id=self.student_id, date=self.date)
        return student_login
