from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.companies_handler import CompaniesHandler


class CompaniesValue(ValueComposite):
	def __init__(self, companies):
		super(CompaniesValue, self).initialize({})
		companies_array = []
		for company in companies:
			company_value = {
				"name": company.name,
				"link": company.link,
				"partnership_tier": company.partnership_tier,
				"business_area": company.business_area,
				"logo": CompaniesHandler.find_image(company.name)
			}
			companies_array.append(company_value)
		self.serialize_with(data=companies_array)
