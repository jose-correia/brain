from jeec_brain.models.student_companies import StudentCompanies


class DeleteStudentCompanyService():

    def __init__(self, student_company: StudentCompanies):
        self.student_company = student_company

    def call(self) -> bool:
        result = self.student_company.delete()
        return result
