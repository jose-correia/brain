from typing import Optional
from jeec_brain.models.student_companies import StudentCompanies


class AddStudentCompanyService(object):
    def __init__(self, student_id, company_id):
        self.student_id = student_id
        self.company_id = company_id

    def call(self) -> Optional[StudentCompanies]:
        student_company = StudentCompanies.create(
            student_id=self.student_id, company_id=self.company_id
        )
        return student_company
