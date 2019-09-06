from .. import bp
from flask import render_template, request, redirect, url_for, current_app

# handlers
from jeec_brain.handlers.companies_handler import CompaniesHandler

# finders
from jeec_brain.finders.companies_finder import CompaniesFinder

# values
from jeec_brain.values.api_error_value import APIErrorValue

from jeec_brain.apps.auth.wrappers import require_admin_login


@bp.route('/companies', methods=['GET'])
@require_admin_login
def companies_dashboard():
    companies_list = CompaniesFinder.get_all()

    if len(companies_list) == 0:
        error = 'No results found'
        return render_template('admin/companies/companies_dashboard.html', companies=None, error=error, search=None)

    return render_template('admin/companies/companies_dashboard.html', companies=companies_list, error=None, search=None)


@bp.route('/companies', methods=['POST'])
@require_admin_login
def search_company():
    name = request.form.get('name')
    companies_list = CompaniesFinder.search_by_name(name)

    if len(companies_list) == 0:
        error = 'No results found'
        return render_template('admin/companies/companies_dashboard.html', companies=None, error=error, search=name)

    return render_template('admin/companies/companies_dashboard.html', companies=companies_list, error=None, search=name)


@bp.route('/new-company', methods=['GET'])
@require_admin_login
def add_company_dashboard():
    return render_template('admin/companies/add_company.html', error=None)


@bp.route('/new-company', methods=['POST'])
@require_admin_login
def create_company():
    name = request.form.get('name')
    link = request.form.get('link')
    email = request.form.get('email')
    business_area = request.form.get('business_area')
    access_cv_platform = request.form.get('access_cv_platform')
    partnership_tier = request.form.get('partnership_tier')

    if partnership_tier == "":
        partnership_tier = None

    if access_cv_platform == 'True':
        access_cv_platform = True
    else:
        access_cv_platform = False

    company = CompaniesHandler.create_company(
        name=name,
        email=email,
        business_area=business_area,
        link=link,
        access_cv_platform=access_cv_platform,
        partnership_tier=partnership_tier
    )
    
    if company is None:
        return render_template('admin/companies/add_company.html', error="Failed to create company! Maybe it already exists :)")

    if 'file' in request.files:
        file = request.files['file']
        result, msg = CompaniesHandler.upload_image(file, name)

        if result == False:
            CompaniesHandler.delete_company(company)
            return render_template('admin/companies/add_company.html', error=msg)

    return redirect(url_for('admin_api.companies_dashboard'))


@bp.route('/company/<string:company_external_id>', methods=['GET'])
@require_admin_login
def get_company(company_external_id):
    company = CompaniesFinder.get_from_external_id(company_external_id)

    image_path = CompaniesHandler.find_image(company.name)

    return render_template('admin/companies/update_company.html', company=company, image=image_path, error=None)


@bp.route('/company/<string:company_external_id>', methods=['POST'])
@require_admin_login
def update_company(company_external_id):

    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)

    name = request.form.get('name')
    link = request.form.get('link')
    email = request.form.get('email')
    business_area = request.form.get('business_area')
    access_cv_platform = request.form.get('access_cv_platform')
    partnership_tier = request.form.get('partnership_tier')

    if partnership_tier == "":
        partnership_tier = None

    if access_cv_platform == 'True':
        access_cv_platform = True
    else:
        access_cv_platform = False

    image_path = CompaniesHandler.find_image(name)

    updated_company = CompaniesHandler.update_company(
        company=company,
        name=name,
        email=email,
        business_area=business_area,
        link=link,
        access_cv_platform=access_cv_platform,
        partnership_tier=partnership_tier
    )
    
    if updated_company is None:
        return render_template('admin/companies/update_company.html', company=company, image=image_path, error="Failed to update company!")

    if 'file' in request.files:
        file = request.files['file']

        result, msg = CompaniesHandler.upload_image(file, name)

        if result == False:
            return render_template('admin/companies/update_company.html', company=updated_company, image=image_path, error=msg)

    return redirect(url_for('admin_api.companies_dashboard'))


@bp.route('/company/<string:company_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_company(company_external_id):
    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)
    
    name = company.name
    
    if CompaniesHandler.delete_company(company):
        CompaniesHandler.delete_image(name)
        return redirect(url_for('admin_api.companies_dashboard'))

    else:
        image_path = CompaniesHandler.find_image(name)
        return render_template('admin/companies/update_company.html', company=company, image=image_path, error="Failed to delete company!")


# @bp.route('/companies/<string:company_external_id>/activities', methods=['GET'])
# @require_admin_login
# def get_company_activities(company_external_id):
#     company = CompaniesFinder.get_from_external_id(company_external_id)

#     if company is None:
#         return APIErrorValue('Couldnt find company').json(500)
        
#     if CompaniesHandler.delete_company(company):
#         return {'message': "Company {} was deleted".format(company.name)}
#     else:
#         return APIErrorValue('Company deletion failed').json(500)


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
