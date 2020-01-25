from jeec_brain.apps.students_api import bp
from flask import Response, send_file, render_template, current_app
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.values.api_error_value import APIErrorValue
from http import HTTPStatus


@bp.route('/resume', methods=['GET'])
#@require_student_login
def resume_dashboard():
    ist_id = current_user.username
    filename = 'cv-' + ist_id + '.pdf'

    user_has_uploaded = FileHandler.check_if_exists(filename)

    return render_template('students/resume.html', ist_id=ist_id, user_has_uploaded=user_has_uploaded, error=None)


@bp.route('/resume', methods=['POST'])
#@require_student_login
def submit_resume():
    ist_id = current_user.username
    filename = 'cv-' + ist_id + '.pdf'
    user_has_uploaded = FileHandler.check_if_exists(filename)

    if 'file' not in request.files:
        error = 'Receiver upload request with no file part'
        current_app.logger.warning(error)
        return render_template('students/resume.html', ist_id=ist_id, user_has_uploaded=user_has_uploaded, error=error)
        
    file = request.files['file']
        
    if file.filename == '':
        error = 'User tried to upload empty file.'
        current_app.logger.warning(error)
        return render_template('students/resume.html', ist_id=ist_id, user_has_uploaded=user_has_uploaded, error=error)

    try:
        FileHandler.upload_file(file, filename)
    except Exception as error:
        current_app.logger.error("Failed to upload file")
        return render_template('students/resume.html', ist_id=ist_id, user_has_uploaded=user_has_uploaded, error=error)
    
    return render_template('students/resume.html', ist_id=ist_id, user_has_uploaded=True, error=None)


@bp.route('/resume/file', methods=['GET'])
#@require_student_login
def get_file():
    ist_id = current_user.username
    filename = 'cv-' + ist_id + '.pdf'

    if not FileHandler.check_if_exists(filename):
        return APIErrorValue("File doesnt exist.").json(HTTPStatus.NOT_FOUND)

    return send_from_directory(os.path.join(current_app.root_path, 'storage'), filename)


@bp.route('/resume/delete', methods=['GET'])
#@require_student_login
def delete_resume():
    ist_id = current_user.username
    filename = 'cv-' + ist_id + '.pdf'

    if not FileHandler.check_if_exists(filename):
        return APIErrorValue("File doesnt exist.").json(HTTPStatus.NOT_FOUND)

    FileHandler.delete_file(filename)
    return redirect(url_for('students_api.resume_dashboard'))
