from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.levels_value import LevelsValue
from jeec_brain.values.squads_value import SquadsValue


class CompanyUsersValue(ValueComposite):
    def __init__(self, company_users):
        super(CompanyUsersValue, self).initialize({})

        company_users_array = []
        for company_user in company_users:
            company_user_value = {
                "name": company_user.user.name,
                "post": company_user.post,
                "user_id": company_user.user.external_id,
            }
            company_users_array.append(company_user_value)

        self.serialize_with(data=company_users_array)
