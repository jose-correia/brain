from .. import bp
from flask import render_template, request

# parsers
from parsers import create_comapny_parser, update_comapny_parser

# handlers
from jeec_brain.handlers.companies_handler import CompaniesHandler

# finders
from jeec_brain.finders.company_finder import CompanyFinder

# values
from jeec_brain.values.company_value import CompanyValue
from jeec_brain.values.api_error_value import APIErrorValue

from jeec_brain.apps.auth.wrappers import require_admin_login


@bp.route('/companies', methods=['GET'])
@require_admin_login
def companies_dashboard():
    companies_list = CompanyFinder.get_all()

    return render_template('admin/companies_dashboard.html', companies=companies_list)


@bp.route('/companies', methods=['POST'])
@require_admin_login
def create_company():
    payload = create_comapny_parser.parse_args()

    company = CompaniesHandler.create_company(
                                    name=payload['name'],
                                    email=payload['email'],
                                    business_area=payload['business_are'],
                                    link=['link']
                                )
    
    if company is None:
        return APIErrorValue('Company creation failed').json(500)

    return CompanyValue(company, details=False).json(200)


@bp.route('/companies/<string:company_external_id>', methods=['PUT'])
@require_admin_login
def update_company(company_external_id):
    payload = update_comapny_parser.parse_args()

    company = CompanyFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)

    updated_company = CompaniesHandler.update_company(payload)
    
    if updated_company is None:
        return APIErrorValue('Company update failed').json(500)

    return CompanyValue(company, details=True).json(200)


@bp.route('/companies/<string:company_external_id>', methods=['DELETE'])
@require_admin_login
def delete_company(company_external_id):
    company = CompanyFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)
        
    if CompaniesHandler.delete_company(company):
        return {'message': "Company {} was deleted".format(company.name)}
    else:
        return APIErrorValue('Company deletion failed').json(500)


@bp.route('/companies/<string:company_external_id>/activities', methods=['GET'])
@require_admin_login
def get_company_activities(company_external_id):
    company = CompanyFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)
        
    if CompaniesHandler.delete_company(company):
        return {'message': "Company {} was deleted".format(company.name)}
    else:
        return APIErrorValue('Company deletion failed').json(500)


# @bp.route('/companies/<string:company_external_id>/activities', methods=['POST'])
# @require_admin_login
# def create_company_activity(company_external_id):
#     company = CompanyFinder.get_from_external_id(company_external_id)

#     if company is None:
#         return APIErrorValue('Couldnt find company').json(500)
        
#     if CompaniesHandler.delete_company(company):
#         return {'message': "Company {} was deleted".format(company.name)}
#     else:
#         return APIErrorValue('Company deletion failed').json(500)


# @bp.route('/companies/<string:company_external_id>/activities', methods=['PUT'])
# @require_admin_login
# def update_company_activity(company_external_id):
#     company = CompanyFinder.get_from_external_id(company_external_id)

#     if company is None:
#         return APIErrorValue('Couldnt find company').json(500)
        
#     if CompaniesHandler.delete_company(company):
#         return {'message': "Company {} was deleted".format(company.name)}
#     else:
#         return APIErrorValue('Company deletion failed').json(500)


# @bp.route('/companies/<string:company_external_id>/activities', methods=['DELETE'])
# @require_admin_login
# def delete_company_activity(company_external_id):
#     company = CompanyFinder.get_from_external_id(company_external_id)

#     if company is None:
#         return APIErrorValue('Couldnt find company').json(500)
        
#     if CompaniesHandler.delete_company(company):
#         return {'message': "Company {} was deleted".format(company.name)}
#     else:
#         return APIErrorValue('Company deletion failed').json(500)
