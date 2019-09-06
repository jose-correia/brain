# SERVICES
import os
from flask import current_app
from jeec_brain.services.companies.create_company_service import CreateCompanyService
from jeec_brain.services.companies.update_company_service import UpdateCompanyService
from jeec_brain.services.companies.delete_company_service import DeleteCompanyService

import logging
logger = logging.getLogger(__name__)


def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGES']


class CompaniesHandler():
    
    @classmethod
    def create_company(cls, **kwargs):
        return CreateCompanyService(payload=kwargs).call()

    @classmethod
    def update_company(cls, company, **kwargs):
        return UpdateCompanyService(company=company, kwargs=kwargs).call()

    @classmethod
    def delete_company(cls, company):
        return DeleteCompanyService(company=company).call()

    @staticmethod
    def upload_image(file, company_name):
        if file.filename == '':
            return False, 'No file selected for uploading'

        if file and allowed_image(file.filename):
            filename = company_name.lower().replace(' ', '_') + '.png'
            try:
                file.save(os.path.join(current_app.root_path, 'static', 'companies', filename))
                return True, None
            
            except Exception as e:
                logger.error(e)
                return False, 'Image upload failed'

        return False, 'File extension is not allowed'

    @staticmethod
    def delete_image(company_name):
        filename = company_name.lower().replace(' ', '_') + '.png'

        try:
            os.remove(os.path.join(current_app.root_path, 'static', 'companies', filename))
            return True
        except Exception as e:
            return False

    @staticmethod
    def find_image(company_name):
        image_filename = company_name.lower().replace(' ', '_') + '.png'
        image_path = f'/static/companies/{image_filename}'

        if not os.path.isfile(os.path.join(current_app.root_path, 'static', 'companies', image_filename)): 
            image_path = None
        else:
            return image_path
