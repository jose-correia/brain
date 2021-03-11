from jeec_brain.apps.companies_api import bp
from flask import Response, send_file, render_template, send_from_directory
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.events_finder import EventsFinder
from datetime import datetime


@bp.route('/resumes', methods=['GET'])
@require_company_login
def resumes_dashboard(company_user):
    if company_user.company.cvs_access:
        event = EventsFinder.get_default_event()
        today = datetime.now()
        cvs_access_start = datetime.strptime(event.cvs_access_start, '%d %b %Y, %a')
        cvs_access_end = datetime.strptime(event.cvs_access_end, '%d %b %Y, %a')

        if today < cvs_access_start or today > cvs_access_end:
            return render_template('companies/resumes/resumes_dashboard.html', cv_students=None, interested_students=None, error="Out of access date")
    else:
        return render_template('companies/resumes/resumes_dashboard.html', cv_students=None, interested_students=None, error="Not authorized")

    company_user = UsersFinder.get_company_user_from_user(current_user)
    interested_students = StudentsFinder.get_company_students(company_user.company)
    cv_students = StudentsFinder.get_cv_students()

    return render_template('companies/resumes/resumes_dashboard.html', cv_students=cv_students, interested_students=interested_students, error=None)

@bp.route('/resumes/<string:student_external_id>/download', methods=['GET'])
@require_company_login
def download_resume(company_user, student_external_id):
    student = StudentsFinder.get_from_external_id(student_external_id)
    if(student is None):
        return render_template('companies/resumes/resumes_dashboard.html', error="Student not found")

    filename = 'cv-' + student.user.username + '.pdf'
    
    return send_from_directory(directory='storage', filename=filename)

@bp.route('/resumes/download', methods=['GET'])
@require_company_login
def download_resumes(company_user):
    zip_file = FileHandler.get_files_zip()
        
    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file,
        as_attachment=True,
        attachment_filename='curriculos_JEEC21.zip')
