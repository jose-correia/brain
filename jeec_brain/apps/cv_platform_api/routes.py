import os
from config import Config
from flask import flash, send_file, redirect, Response, url_for, render_template, session, request, send_from_directory, current_app
from . import bp

from .handlers.file_handler import FileHandler

from jeec_brain.apps.auth.wrappers import require_api_token
from flask_login import login_required


import logging
logger = logging.getLogger(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@bp.route('/')
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/')
@bp.route('/index', methods=['POST'])
def choose_role():
    if request.form['submit'] == 'Fenix Authentication':
        return redirect(url_for('auth.login'))
    
    elif request.form['submit'] == 'Company Authentication':
        return redirect(url_for('auth.get_company_login_form'))
    
    return redirect(url_for('cv_platform_api_bp.company_dashboard'))


# route for the company dashboard
@bp.route('/company_dashboard', methods=['GET'])
@login_required
def company_dashboard():
    logger.info('entered dashboard!')
    company_name = session['name']
    company_logo = '/static/partner-logos/' + company_name.lower() + '.png'

    return render_template('company_dashboard.html', name=company_name, logo=company_logo)
        

# routes for the students dashboard
@bp.route('/student_dashboard', methods=['GET'])
@require_api_token
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
@require_api_token
def student_dashboard_actions():
    if request.form['submit'] == 'Check':
        return redirect(url_for('cv_platform_api.uploaded_file'))
    
    elif request.form['submit'] == 'Delete':
        return redirect(url_for('cv_platform_api.delete_file'))
    
    # elif request.form['submit'] == 'Upload':
    #     if 'file' not in request.files:
    #         logger.warning('Receiver upload request with no file part')
    #         return redirect(request.url)
        
    #     file = request.files['file']
        
    #     if file.filename == '':
    #         logger.warning('User tried to upload empty file')
    #         return redirect(request.url)

    #     if file and allowed_file(file.filename):
    #         filename = 'cv-' + session['username'] + '.pdf'

    #         FileHandler.upload_file(file, filename)
    #         logger.info('File uploaded sucessfuly!')
        
    #     elif not allowed_file(file.filename):
    #         logger.warning('Wrong file extension')
    #         flash('Upload .pdf')
    #         return redirect(request.url)
            
    #     return redirect(url_for('cv_platform_api.dashboard'))
    
    elif request.form['submit'] == 'Accept Terms':
        from jeec_brain.models.student import Student
        student = Student.query.filter_by(istid=session['username']).first()
        student.update(acceptedTerms=True)
        session['first_time_login'] = False
        student.reload()
        return redirect(request.url)
    
    return redirect(url_for('cv_platform_api.student_dashboard'))


# routes for file handling
@bp.route('/delete', methods=['GET'])
@require_api_token
def delete_file():
    filename = 'cv-' + session['username'] + '.pdf'
    FileHandler.delete_file(filename)
    return redirect(url_for('cv_platform_api.dashboard'))
    

@bp.route('/uploaded', methods=['GET'])
@require_api_token
def uploaded_file():
    filename = 'cv-' + session['username'] + '.pdf'
    return send_from_directory(os.path.join(current_app.root_path, 'storage'), filename)


# content routes
@bp.route('/company_dashboard/download', methods=['GET', 'POST'])
@login_required
def download_files():
    zip_file = FileHandler.get_files_zip()
        
    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file,
        as_attachment=True,
        attachment_filename='curriculos_JEEC19.zip')
