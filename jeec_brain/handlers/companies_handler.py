# SERVICES
from flask import current_app
from jeec_brain.services.companies.create_company_service import CreateCompanyService
from jeec_brain.services.companies.update_company_service import UpdateCompanyService
from jeec_brain.services.companies.delete_company_service import DeleteCompanyService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from jeec_brain.services.chat.create_channel_service import CreateChannelService
from jeec_brain.services.chat.delete_channel_service import DeleteChannelService
from jeec_brain.services.mail.send_mail_service import SendMailService


class CompaniesHandler:
    @classmethod
    def create_company(cls, chat_enabled, **kwargs):
        print("here", chat_enabled, type(chat_enabled))
        if chat_enabled:
            name = kwargs.get("name", None)
            chat_id, chat_code = CreateChannelService(name).call()
            if not chat_id or not chat_code:
                return None
        else:
            chat_id = None
            chat_code = None

        return CreateCompanyService(
            kwargs={**kwargs, **{"chat_id": chat_id, "chat_code": chat_code}}
        ).call()

    @classmethod
    def update_company(cls, chat_enabled, company, **kwargs):
        if chat_enabled:
            if not company.chat_id:
                chat_id, chat_code = CreateChannelService(
                    company.name.replace("&", " and ")
                ).call()
                if not chat_id or not chat_code:
                    return None
            else:
                chat_id = company.chat_id
                chat_code = company.chat_code

            return UpdateCompanyService(
                company=company,
                kwargs={**kwargs, **{"chat_id": chat_id, "chat_code": chat_code}},
            ).call()

        return UpdateCompanyService(company=company, kwargs=kwargs).call()

    @classmethod
    def delete_company(cls, chat_enabled, company):
        company_name = company.name

        if chat_enabled:
            result = DeleteChannelService(company.chat_id).call()
            if not result:
                return False

        if DeleteCompanyService(company=company).call():
            for extension in current_app.config["ALLOWED_IMAGES"]:
                filename = company_name.lower().replace(" ", "_") + "." + extension
                DeleteImageService(filename, "static/companies/images").call()
            return True
        return False

    @classmethod
    def upload_image(cls, file, company_name):
        return UploadImageService(file, company_name, "static/companies/images").call()

    @classmethod
    def find_image(cls, company_name):
        return FindImageService(company_name, "static/companies/images").call()

    @classmethod
    def send_mail_to_company_users(cls, company_users, subject, content):
        return SendMailService(
            [user.user.email for user in company_users], subject, content
        ).call()
