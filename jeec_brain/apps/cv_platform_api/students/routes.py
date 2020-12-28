import os
from config import Config
from flask import flash, redirect, url_for, render_template, session, request, send_from_directory, current_app
from .. import bp

from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler

import logging
logger = logging.getLogger(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# Student login
@bp.route('/login-student')
def login_student():
    return AuthHandler.redirect_to_fenix_login()

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(url_for('/'))
    
    fenix_auth_code = request.args.get('code')

    if AuthHandler.login_student(fenix_auth_code) is True:
        return redirect(url_for('cv_platform_api_bp.student_dashboard'))

    else:
        return redirect(url_for('/'))

# routes for the students dashboard
@bp.route('/student_dashboard', methods=['GET'])
@require_student_login
def student_dashboard():
    if session['first_time_login'] == True:
        return render_template('terms_conditions.html')

    else:
        filename = 'cv-' + session['username'] + '.pdf'

        if os.path.isfile(os.path.join(current_app.root_path, 'storage', filename)): 
            has_uploaded = True
        else:
            has_uploaded = False

        return render_template('user_dashboard.html', name=session['name'], username=session['username'], has_uploaded=has_uploaded, first_time_login=session['first_time_login'])


@bp.route('/student_dashboard', methods=['POST'])
@require_student_login
def student_dashboard_actions():
    if request.form['submit'] == 'Check':
        return redirect(url_for('cv_platform_api.uploaded_file'))
    
    elif request.form['submit'] == 'Delete':
        return redirect(url_for('cv_platform_api.delete_file'))

    elif request.form['submit'] == 'Upload' and Config.CV_SUBMISSION_OPEN is True:
        if 'file' not in request.files:
            logger.warning('Receiver upload request with no file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            logger.warning('User tried to upload empty file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'cv-' + session['username'] + '.pdf'

            FileHandler.upload_file(file, filename)
            logger.info('File uploaded sucessfuly!')
        
        elif not allowed_file(file.filename):
            logger.warning('Wrong file extension')
            flash('Upload .pdf')
            return redirect(request.url)
            
        return redirect(url_for('cv_platform_api.dashboard'))
    
    elif request.form['submit'] == 'Accept Terms':
        from jeec_brain.models.students import Student
        student = Student.query.filter_by(ist_id=session['username']).first()
        student.update(acceptedTerms=True)
        session['first_time_login'] = False
        student.reload()
        return redirect(request.url)
    
    return redirect(url_for('cv_platform_api.student_dashboard'))


# routes for file handling
@bp.route('/delete', methods=['GET'])
@require_student_login
def delete_file():
    filename = 'cv-' + session['username'] + '.pdf'
    FileHandler.delete_file(filename)
    return redirect(url_for('cv_platform_api.dashboard'))
    

@bp.route('/uploaded', methods=['GET'])
@require_student_login
def uploaded_file():
    filename = 'cv-' + session['username'] + '.pdf'
    return send_from_directory(os.path.join(current_app.root_path, 'storage'), filename)