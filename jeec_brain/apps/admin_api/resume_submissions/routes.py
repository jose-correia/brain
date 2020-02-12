from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.resume_submissions_finder import ResumeSubmissionsFinder
from jeec_brain.handlers.resume_submissions_handler import ResumeSubmissionsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.values.api_error_value import APIErrorValue


# Resumes routes
@bp.route('/resume_submissions', methods=['GET'])
@allowed_roles(['admin'])
def resume_submissions_dashboard():
    submissions_list = ResumeSubmissionsFinder.get_all()
    
    if submissions_list is None:
        error = 'No results found'
        return render_template('admin/resume_submissions/submissions_dashboard.html', resumes=None, error=error)

    return render_template('admin/resume_submissions/submissions_dashboard.html', submissions=submissions_list, error=None)


@bp.route('/resume_submissions/new', methods=['GET'])
@allowed_roles(['admin'])
def add_resume_submission_dashboard():
    return render_template('admin/resume_submissions/add_submission.html', error=None)


@bp.route('/resume_submissions/new', methods=['POST'])
@allowed_roles(['admin'])
def create_resume_submission():
    name = request.form.get('name')
    allow_download = request.form.get('allow_download')
    allow_submission = request.form.get('allow_submission')

    if allow_download == 'True':
        allow_download = True
    else:
        allow_download = False

    if allow_submission == 'True':
        allow_submission = True
    else:
        allow_submission = False

    # create new resumes submission
    submission = ResumeSubmissionsHandler.create_submission(
            name=name,
            allow_download=allow_download,
            allow_submission=allow_submission
        )

    if submission is None:
        return render_template('admin/resume_submissions/add_submission.html', error="Failed to create resumes submission!")

    return redirect(url_for('admin_api.resume_submissions_dashboard'))


@bp.route('/resume_submissions/<string:submission_external_id>', methods=['GET'])
@allowed_roles(['admin'])
def get_resumes_submission(submission_external_id):
    submission = ResumeSubmissionsFinder.get_submission_by_external_id(submission_external_id)

    if submission is None:
        error = 'Non existant resumes submission'
        return render_template('admin/resume_submissions/submissions_dashboard.html', submission=None, error=error)

    return render_template('admin/resume_submissions/update_submission.html', \
        submission=submission, \
        error=None)


@bp.route('/resume_submissions/<string:submission_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_resume_submission_submission(submission_external_id):
    submission = ResumeSubmissionsFinder.get_submission_by_external_id(submission_external_id)

    if submission is None:
        return APIErrorValue('Couldnt find submission').json(400)

    name = request.form.get('name')
    allow_download = request.form.get('allow_download')
    allow_submission = request.form.get('allow_submission')

    if allow_download == 'True':
        allow_download = True
    else:
        allow_download = False

    if allow_submission == 'True':
        allow_submission = True
    else:
        allow_submission = False

    updated_submission = ResumeSubmissionsHandler.update_submission(
        submission=submission,
        name=name,
        allow_download=allow_download,
        allow_submission=allow_submission
    )
    
    if updated_submission is None:
        return render_template('admin/resume_submissions/update_submission.html', \
            submission=submission, \
            error="Failed to update submission!")

    return redirect(url_for('admin_api.resume_submissions_dashboard'))


@bp.route('/resume_submissions/<string:submission_external_id>/delete', methods=['GET'])
@allowed_roles(['admin'])
def delete_resume_submission(submission_external_id):
    submission = ResumeSubmissionsFinder.get_submission_by_external_id(submission_external_id)

    if submission is None:
        return APIErrorValue('Couldnt find submission').json(400)
        
    if not ResumeSubmissionsHandler.delete_submission(auction):
        return render_template('admin/resume_submissions/update_submission.html', submission=submission, error="Failed to delete submission!")

    return redirect(url_for('admin_api.resume_submissions_dashboard'))


# Participants management
@bp.route('/resume_submissions/<string:submission_external_id>/participants', methods=['GET'])
@allowed_roles(['admin'])
def resume_submission_participants_dashboard(submission_external_id):
    submission = ResumeSubmissionsFinder.get_submission_by_external_id(submission_external_id)

    if submission is None:
        return APIErrorValue('Couldnt find submission').json(400)

    not_participants = ResumeSubmissionsFinder.get_not_participants(submission)

    if len(submission.participants) == 0:
        error = 'No results found'
        return render_template('admin/resume_submissions/submission_participants_dashboard.html', submission=submission, not_participants=not_participants, error=error)

    return render_template('admin/resume_submissions/submission_participants_dashboard.html', submission=submission, not_participants=not_participants, error=None)


@bp.route('/resume_submissions/<string:submission_external_id>/add-participant', methods=['POST'])
@allowed_roles(['admin'])
def add_resume_submission_participant(submission_external_id):
    submission = ResumeSubmissionsFinder.get_submission_by_external_id(submission_external_id)

    if submission is None:
        return APIErrorValue('Couldnt find submission').json(400)

    company_external_id = request.form.get('company_external_id')

    if company_external_id is None:
        return redirect(url_for('admin_api.resume_submission_participants_dashboard', submission_external_id=submission_external_id))

    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(400)

    ResumeSubmissionsHandler.add_submission_participant(submission, company)
    
    return redirect(url_for('admin_api.resume_submission_participants_dashboard', submission_external_id=submission_external_id))
