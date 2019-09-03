# SERVICES
from jeec_brain.services.companies.create_company_service import CreateCompanyService
from jeec_brain.services.update_data_service import UpdateDataService
from jeec_brain.services.companies.delete_company_service import DeleteCompanyService


class CompaniesHandler(object):
    @classmethod
    def create_company(cls, name, email, business_area, link):
        return CreateCompanyService(
            name=name, email=email, business_area=business_area, link=link).call()

    @classmethod
    def update_company(cls, company, **kwargs):
        return UpdateDataService(data_model=company, kwargs=kwargs).call()

    @classmethod
    def delete_company(cls, company, **kwargs):
        return DeleteCompanyService(company=company).call()

    # @classmethod
    # def upload_logo(file, filename):
    #     try:
    #         file.save(os.path.join(current_app.root_path, 'storage', filename))
    #         return True
    #     except Exception as e:
    #         logger.error(e)
