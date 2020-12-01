from . import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, session, jsonify
from flask_login  import current_user, login_required
from config import Config

# Handlers
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.squads_handler import SquadsHandler

# Finders
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder

# Values
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.values.students_value import StudentsValue
from jeec_brain.values.squads_value import SquadsValue
from jeec_brain.values.squad_invitations_value import SquadInvitationsValue

from jeec_brain.apps.auth.wrappers import requires_student_auth

# Login routes
@bp.route('/login')
def login_student():
    return AuthHandler.redirect_to_fenix_login()

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(Config.STUDENT_APP_URL + 'login')
    
    fenix_auth_code = request.args.get('code')

    loggedin, jwt = AuthHandler.login_student(fenix_auth_code)
    
    if loggedin is True:
        return redirect(Config.STUDENT_APP_URL + '?jwt=' + str(jwt, 'utf-8'))

    else:
        return redirect(Config.STUDENT_APP_URL)

@bp.route('/info', methods=['GET'])
@requires_student_auth
def get_info(student):    
    return StudentsValue(student, details=True).json(200)

@bp.route('/students', methods=['GET'])
@requires_student_auth
def get_students(student):
    search = request.args.get('search', None)

    students = StudentsFinder.get_from_search_without_student(search, student.external_id)

    return StudentsValue(students, details=False).json(200)

@bp.route('/squad', methods=['GET'])
@requires_student_auth
def get_squad(student):
    if(student.squad is None):
        return APIErrorValue('No squad found').json(404)
    
    return SquadsValue(student.squad).json(200)

@bp.route('/squad', methods=['POST'])
@requires_student_auth
def create_squad(student):
    if(student.squad is not None):
        return APIErrorValue('Student already has squad').json(401)

    name = request.form.get('name', None)
    cry = request.form.get('cry', None)
    
    if name is None or cry is None:
        return APIErrorValue('Invalid squad info').json(500)

    if 'file' not in request.files:
        return APIErrorValue('No image detected').json(500)

    file = request.files['file']

    if file and file.filename != '':
        result, msg = SquadsHandler.upload_squad_image(file, name)
    
        if not result:
            return APIErrorValue(msg).json(500)

        squad = SquadsHandler.create_squad(name=name, cry=cry, captain_ist_id=student.ist_id)
        StudentsHandler.add_squad_member(student, squad)

    else:
        return APIErrorValue('No image found').json(500)
    
    return SquadsValue(squad).json(200)

@bp.route('/invite-squad', methods=['POST'])
@requires_student_auth
def invite_squad(student):
    if(student.squad is None):
        return APIErrorValue('No squad found').json(401)

    try:
        members = request.get_json()["members"]
    except KeyError:
        return APIErrorValue('Invalid members').json(500)

    if(StudentsHandler.invite_squad_members(student, members)):
        return jsonify('Success'), 200
    else:
        return APIErrorValue('Failed to invite').json(500)

@bp.route('/squad-invitations', methods=['GET'])
@requires_student_auth
def get_squad_invitations(student):
    invitations = SquadsFinder.get_invitations_from_parameters({"receiver_id": student.id})

    return SquadInvitationsValue(invitations).json(200)

@bp.route('/accept-invitation', methods=['POST'])
@requires_student_auth
def accept_invitation(student):
    try:
        invitation_id = request.get_json()["invitation_id"]
    except KeyError:
        return APIErrorValue('Invalid invitation').json(500)

    invitation = SquadsFinder.get_invitation_from_external_id(invitation_id)
    if(invitation is None):
        return APIErrorValue('Invitation not found').json(404)

    student = StudentsHandler.accept_invitation(student, invitation)

    return StudentsValue(student, details=True).json(200)

@bp.route('reject-invitation', methods=['POST'])
@requires_student_auth
def reject_invitation(student):
    try:
        invitation_id = request.get_json()["invitation_id"]
    except KeyError:
        return APIErrorValue('Invalid invitation').json(500)

    invitation = SquadsFinder.get_invitation_from_external_id(invitation_id)
    if(invitation is None):
        return APIErrorValue('Invitation not found').json(404)

    SquadsHandler.delete_squad_invitation(invitation)

    return jsonify('Success'), 200

@bp.route('leave-squad', methods=['POST'])
@requires_student_auth
def leave_squad(student):
    student = StudentsHandler.leave_squad(student)

    return StudentsValue(student, details=True).json(200)

@bp.route('kick-member', methods=['POST'])
@requires_student_auth
def kick_member(student):
    if(not student.is_captain()):
        return APIErrorValue('Student is not captain').json(401)

    try:
        member_ist_id = request.get_json()["ist_id"]
    except KeyError:
        return APIErrorValue('Invalid IST id').json(500)
    
    member = StudentsFinder.get_from_ist_id(member_ist_id)
    if(member is None):
        return APIErrorValue('Member not found').json(404)

    StudentsHandler.leave_squad(member)

    return SquadsValue(student.squad).json(200)

@bp.route('/redeem-code', methods=['POST'])
@requires_student_auth
def redeem_code(student):
    try:
        code = request.get_json()["code"]
    except KeyError:
        return APIErrorValue('Invalid code').json(500)

    student = ActivityCodesHandler.redeem_activity_code(student, code)

    if(student is None):
        return APIErrorValue('Invalid code').json(500)

    return StudentsValue(student, details=True).json(200)

@bp.route('/add-linkedin', methods=['POST'])
@requires_student_auth
def add_linkedin(student):
    try:
        url = request.get_json()["url"]
    except KeyError:
        return APIErrorValue('Invalid url').json(500)

    student = StudentsHandler.add_linkedin(student, url)

    return StudentsValue(student, details=True).json(200)

@bp.route('/add-cv', methods=['POST'])
@requires_student_auth
def add_cv(student):
    if 'cv' not in request.files:
        return APIErrorValue('No cv found').json(500)

    file = request.files['file']
    if file.filename == '':
        return APIErrorValue('No cv found').json(500)

    if file and allowed_file(file.filename):
        filename = 'cv-' + student.ist_id + '.pdf'

        # FileHandler.upload_file(file, filename)
        # logger.info('File uploaded sucessfuly!')

    else:
        return APIErrorValue('Wrong file extension').json(500)

    return StudentsValue(student, details=True).json(200)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS