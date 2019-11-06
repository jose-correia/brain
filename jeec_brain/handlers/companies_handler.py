# SERVICES
from flask import current_app
from jeec_brain.services.companies.create_company_service import CreateCompanyService
from jeec_brain.services.companies.update_company_service import UpdateCompanyService
from jeec_brain.services.companies.delete_company_service import DeleteCompanyService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService


class CompaniesHandler():
    
    @classmethod
    def create_company(cls, **kwargs):
        return CreateCompanyService(kwargs=kwargs).call()

    @classmethod
    def update_company(cls, company, **kwargs):
        return UpdateCompanyService(company=company, kwargs=kwargs).call()

    @classmethod
    def delete_company(cls, company):
        company_name = company.name

        if DeleteCompanyService(company=company).call():
            for extension in current_app.config['ALLOWED_IMAGES']:
                filename = company_name.lower().replace(' ', '_') + '.' + extension
                DeleteImageService(filename, 'static/companies/images').call()
            return True
        return False

    @classmethod
    def upload_image(cls, file, company_name):
        return UploadImageService(file, company_name, 'static/companies/images').call()

    @classmethod
    def find_image(cls, company_name):
        return FindImageService(company_name, 'static/companies/images').call()
