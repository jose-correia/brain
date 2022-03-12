from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.companies_handler import CompaniesHandler


class CompaniesValue(ValueComposite):
    def __init__(self, companies, details):
        super(CompaniesValue, self).initialize({})
        companies_array = []
        for company in companies:
            company_value = {
                "name": company.name,
                "partnership_tier": company.partnership_tier,
                "logo": CompaniesHandler.find_image(company.name),
            }
            if details:
                company_details = {
                    "link": company.link,
                    "business_area": company.business_area,
                }
                companies_array.append({**company_value, **company_details})
            else:
                companies_array.append(company_value)

        self.serialize_with(data=companies_array)
