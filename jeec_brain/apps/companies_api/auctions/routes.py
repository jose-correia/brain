from jeec_brain.apps.companies_api import bp
from flask import Response, render_template
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler


@bp.route('/auction', methods=['GET'])
@require_company_login
def auction_dashboard():
    # TODO
    return render_template('companies/auction/auction_dashboard.html', companies=companies_list, error=None, search=None, role=current_user.role.name)


@bp.route('/auction/bid', methods=['POST'])
@require_company_login
def auction_bid():
    # TODO
    zip_file = FileHandler.get_files_zip()
        
    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file,
        as_attachment=True,
        attachment_filename='curriculos_JEEC19.zip')
