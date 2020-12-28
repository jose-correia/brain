from typing import Dict, Optional
from jeec_brain.models.student_companies import StudentCompanies


class UpdateStudentCompanyService():
    
    def __init__(self, student_company: StudentCompanies, kwargs: Dict):
        self.student_company = student_company
        self.kwargs = kwargs

    def call(self) -> Optional[StudentCompanies]:
        update_result = self.student_company.update(**self.kwargs)
        return update_result
