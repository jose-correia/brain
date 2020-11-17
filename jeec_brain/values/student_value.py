from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.values.levels_value import LevelsValue
from jeec_brain.values.squads_value import SquadsValue

class StudentValue(ValueComposite):
    def __init__(self, student, details=True):
        super(StudentValue, self).initialize({})
        
        self.serialize_with(name=student.name)
        self.serialize_with(username=student.user.username)
        self.serialize_with(email=student.user.email)
        self.serialize_with(photo=student.photo)
        self.serialize_with(photo_type=student.photo_type)
        self.serialize_with(daily_points=student.daily_points)
        self.serialize_with(total_points=student.total_points)
        self.serialize_with(squad_points=student.squad_points)
        self.serialize_with(level=LevelsValue(student.level).to_dict())
        self.serialize_with(linkedin_url=student.linkedin_url)
        self.serialize_with(uploaded_cv=student.uploaded_cv)

        if details:
            favorite_companies = []
            for company in student.stared_companies:
                favorite_companies.append({
                    "company": CompaniesValue(company).to_dict(),
                })

            self.serialize_with(favorite_companies=favorite_companies)
            self.serialize_with(accepted_terms=student.accepted_terms)
