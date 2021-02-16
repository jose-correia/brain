from typing import Dict, Optional
from jeec_brain.models.student_logins import StudentLogins


class UpdateStudentLoginService():
    
    def __init__(self, student_login: StudentLogins, kwargs: Dict):
        self.student_login = student_login
        self.kwargs = kwargs

    def call(self) -> Optional[StudentLogins]:
        update_result = self.student_login.update(**self.kwargs)
        return update_result
