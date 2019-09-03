from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.company_value import CompanyValue


class StudentValue(ValueComposite):
    def __init__(self, student, details=True):
        super(StudentValue, self).initialize({})
        self.serialize_with(name=student.name)
        self.serialize_with(username=student.user.username)
        self.serialize_with(istid=student.istid)

        if details:
            favorite_companies = []
            for company in student.stared_companies:
                favorite_companies.append({
                    "company": CompanyValue(company, details=False).to_dict(),
                })

            self.serialize_with(favorite_companies=favorite_companies)
            self.serialize_with(accepted_terms=student.accepted_terms)
