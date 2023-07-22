from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.company_users_value import CompanyUsersValue
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder


class PartnersValue(ValueComposite):
    def __init__(self, partner, student):
        super(PartnersValue, self).initialize({})

        self.serialize_with(name=partner.name)
        self.serialize_with(business_area=partner.business_area)
        self.serialize_with(logo=CompaniesHandler.find_image(partner.name))
        self.serialize_with(team=CompanyUsersValue(partner.users).to_dict())
        self.serialize_with(interest=partner in student.companies)
        self.serialize_with(zoom_url=None)
