from jeec_brain.apps.companies_api import bp
from flask import Response, send_file, render_template
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.handlers.file_handler import FileHandler


@bp.route('/resume', methods=['GET'])
@require_student_login
def resume_dashboard():
    # TODO
    # students_interested = StudentsFinder
    # number_of_resumes = count
    
    return render_template('students/resumes/resume_dashboard.html', error=None)


@bp.route('/resume', methods=['POST'])
@require_student_login
def submit_resume():
    # TODO
    # students_interested = StudentsFinder
    # number_of_resumes = count
    
    return render_template('students/resumes/resume_dashboard.html', error=None)


@bp.route('/resume/file', methods=['GET'])
@require_student_login
def get_file():
    filename = 'cv-' + session['username'] + '.pdf'
    return send_from_directory(os.path.join(current_app.root_path, 'storage'), filename)


@bp.route('/resume/delete', methods=['GET'])
@require_student_login
def delete_resume():
    # TODO
    filename = 'cv-' + session['username'] + '.pdf'
    FileHandler.delete_file(filename)
    return redirect(url_for('cv_platform_api.dashboard'))
    

@bp.route('/resume/download', methods=['GET'])
@require_student_login
def download_resume():
    # TODO
    zip_file = FileHandler.get_files_zip()
        
    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file,
        as_attachment=True,
        attachment_filename='curriculos_JEEC19.zip')
