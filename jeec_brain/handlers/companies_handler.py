# SERVICES
from jeec_brain.services.companies.create_company_service import CreateCompanyService
from jeec_brain.services.companies.update_company_service import UpdateCompanyService
from jeec_brain.services.companies.delete_company_service import DeleteCompanyService


class CompaniesHandler():
    
    @classmethod
    def create_company(cls, **kwargs):
        return CreateCompanyService(kwargs=kwargs).call()

    @classmethod
    def update_company(cls, company, **kwargs):
        return UpdateCompanyService(company=company, kwargs=kwargs).call()

    @classmethod
    def delete_company(cls, company):
        return DeleteCompanyService(company=company).call()

    # @classmethod
    # def upload_logo(file, filename):
    #     try:
    #         file.save(os.path.join(current_app.root_path, 'storage', filename))
    #         return True
    #     except Exception as e:
    #         logger.error(e)
    
