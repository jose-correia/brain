from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.companies_value import CompaniesValue


class StudentValue(ValueComposite):
    def __init__(self, student, details=True):
        super(StudentValue, self).initialize({})
        self.serialize_with(name=student.name)
        self.serialize_with(username=student.user.username)
        self.serialize_with(email=student.user.email)
        self.serialize_with(photo=student.photo)
        self.serialize_with(photo_type=student.photo_type)

        if details:
            favorite_companies = []
            for company in student.stared_companies:
                favorite_companies.append({
                    "company": CompaniesValue(company).to_dict(),
                })

            self.serialize_with(favorite_companies=favorite_companies)
            self.serialize_with(accepted_terms=student.accepted_terms)
