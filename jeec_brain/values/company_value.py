from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.activity_value import ActivityValue


class CompanyValue(ValueComposite):
	def __init__(self, organization, details=False):
		super(CompanyValue, self).initialize({})
		self.serialize_with(name=str(organization.name))		
		self.serialize_with(link=organization.link)
		self.serialize_with(business_area=organization.business_area)
		self.serialize_with(email=organization.email)

		if details:
			activities_array = []
			for activity in organization.activities:
				activities_array.append({
					"activity": ActivityValue(activity).to_dict(),
				})

			self.serialize_with(username=organization.user.username)
			self.serialize_with(activities=activities_array)
			self.serialize_with(access_cv_platform=organization.access_cv_platform)

		
