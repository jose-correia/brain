from jeec_brain.apps.companies_api import bp
from flask import Response, send_file
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler


@bp.route('/resumes', methods=['GET'])
@require_company_login
def resumes_dashboard():
    # TODO
    # students_interested = StudentsFinder
    # number_of_resumes = count
    
    return render_template('companies/resumes/resumes_dashboard.html', error=None)


@bp.route('/resumes/download', methods=['GET'])
@require_company_login
def download_resumes():
    # TODO
    zip_file = FileHandler.get_files_zip()
        
    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file,
        as_attachment=True,
        attachment_filename='curriculos_JEEC19.zip')
