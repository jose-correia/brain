from jeec_brain.models.company_users import CompanyUsers


class CreateCompanyUserService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        company_user = CompanyUsers.create(**self.kwargs)

        if not company_user:
            return None

        return company_user
