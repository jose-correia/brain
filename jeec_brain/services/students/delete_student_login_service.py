from jeec_brain.models.student_logins import StudentLogins


class DeleteStudentLoginService():

    def __init__(self, student_login: StudentLogins):
        self.student_login = student_login

    def call(self) -> bool:
        result = self.student_login.delete()
        return result
