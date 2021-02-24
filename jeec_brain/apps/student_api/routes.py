from . import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, jsonify, send_file
from flask_login import current_user, login_required
from config import Config
from datetime import datetime
import os
import base64

# Handlers
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.squads_handler import SquadsHandler
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.handlers.file_handler import FileHandler

# Finders
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.users_finder import UsersFinder

# Values
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.values.students_value import StudentsValue
from jeec_brain.values.squads_value import SquadsValue
from jeec_brain.values.squad_invitations_value import SquadInvitationsValue
from jeec_brain.values.student_activities_value import StudentActivitiesValue
from jeec_brain.values.student_activity_types_value import StudentActivityTypesValue
from jeec_brain.values.rewards_value import RewardsValue
from jeec_brain.values.squads_rewards_value import SquadsRewardsValue
from jeec_brain.values.jeecpot_rewards_value import JeecpotRewardsValue
from jeec_brain.values.levels_value import LevelsValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.values.partners_value import PartnersValue

from jeec_brain.apps.auth.wrappers import requires_student_auth

# Login routes
@bp.route('/login')
def login_student():
    return AuthHandler.redirect_to_fenix_login()

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(Config.STUDENT_APP_URL)
    
    fenix_auth_code = request.args.get('code')

    student, encrypted_code = AuthHandler.login_student(fenix_auth_code)
    
    if student:
        now = datetime.utcnow()
        date = now.strftime('%d %b %Y, %a')
        event = EventsFinder.get_default_event()
        dates = EventsHandler.get_event_dates(event)

        if date in dates:
            student_login = StudentsFinder.get_student_login(student, date)
            if student_login:
                return redirect(Config.STUDENT_APP_URL + '?code=' + encrypted_code)
            else:
                StudentsHandler.add_student_login(student, date)
                StudentsHandler.add_points(student, 5)
                return redirect(Config.STUDENT_APP_URL + '?code=' + encrypted_code + '&firstlog=true')
        else:
            return redirect(Config.STUDENT_APP_URL + '?code=' + encrypted_code)

    else:
        return redirect(Config.STUDENT_APP_URL)

@bp.route('/today-login', methods=['GET'])
@requires_student_auth
def today_login(student):
    now = datetime.utcnow()
    date = now.strftime('%d %b %Y, %a')
    event = EventsFinder.get_default_event()
    dates = EventsHandler.get_event_dates(event)

    if date in dates:
        student_login = StudentsFinder.get_student_login(student, date)
        if student_login is None:
            StudentsHandler.add_student_login(student, date)
            StudentsHandler.add_points(student, 5)
        else:
            return APIErrorValue("Already loggedin today").json(409)
    else:
        return APIErrorValue("Date out of event").json(409)
            
    return StudentsValue(student, details=True).json(200)

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

@bp.route('/levels', methods=['GET'])
@requires_student_auth
def get_levels(student):
    levels = LevelsFinder.get_all_levels()

    return LevelsValue(levels, True).json(200)

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
        squad = SquadsHandler.create_squad(name=name, cry=cry, captain_ist_id=student.user.username)
        if squad is None:
            return APIErrorValue('Error creating squad').json(500)

        result, msg = SquadsHandler.upload_squad_image(file, str(squad.external_id))
        if not result:
            SquadsHandler.delete_squad(squad)
            return APIErrorValue(msg).json(500)
        
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
        code = request.get_json()["code"].replace("-","")
    except KeyError:
        return APIErrorValue('Invalid code').json(500)

    result, student = ActivityCodesHandler.redeem_activity_code(student, code)

    if(not result):
        sender_student = StudentsFinder.get_from_referral_code(code)
        if(not sender_student or sender_student.id == student.id):
            return APIErrorValue('Invalid code').json(500)

        result, student = StudentsHandler.redeem_referral(student, sender_student)

        if not result:
            return APIErrorValue('Invalid code').json(500)

    return StudentsValue(student, details=True).json(200)

@bp.route('/activities', methods=['GET'])
@requires_student_auth
def get_activities(student):
    event = EventsFinder.get_default_event()
    
    return StudentActivitiesValue(event, event.activities, student).json(200)

@bp.route('/quests', methods=['GET'])
@requires_student_auth
def get_quests(student):
    event = EventsFinder.get_default_event()
    activities = ActivitiesFinder.get_quests()
    
    return StudentActivitiesValue(event, activities, student, True).json(200)

@bp.route('/activity-types', methods=['GET'])
@requires_student_auth
def get_activity_types(student):
    event = EventsFinder.get_default_event()
    
    return StudentActivityTypesValue(event.activity_types).json(200)

@bp.route('/add-linkedin', methods=['POST'])
@requires_student_auth
def add_linkedin(student):
    try:
        url = request.get_json()["url"]
    except KeyError:
        return APIErrorValue('Invalid url').json(500)

    if not student.linkedin_url:
        StudentsHandler.add_points(student, 10)
    StudentsHandler.update_student(student, linkedin_url=url)

    return StudentsValue(student, details=True).json(200)

@bp.route('/add-cv', methods=['POST'])
@requires_student_auth
def add_cv(student):
    if 'cv' not in request.files:
        return APIErrorValue('No cv found').json(500)

    file = request.files['cv']
    if file.filename == '':
        return APIErrorValue('No cv found').json(500)

    if file and FileHandler.allowed_file(file.filename):
        filename = 'cv-' + student.user.username + '.pdf'

        if not FileHandler.upload_file(file, filename):
            return APIErrorValue('Error uploading file').json(500)

        if not student.uploaded_cv:
            StudentsHandler.update_student(student, uploaded_cv=True)
            StudentsHandler.add_points(student, 10)

    else:
        return APIErrorValue('Wrong file extension').json(500)

    return StudentsValue(student, details=True).json(200)

@bp.route('/cv', methods=['GET'])
@requires_student_auth
def get_cv(student):
    if not student.uploaded_cv:
        return APIErrorValue("No CV uploaded").json(404)

    filename = 'cv-' + student.user.username + '.pdf'

    with open(os.path.join(current_app.root_path, 'storage', filename), mode='rb') as file:
        fileContent = file.read()

    return jsonify({'data':str(base64.b64encode(fileContent), 'utf-8'), 'content-type':'application/pdf'})

@bp.route('/tags', methods=['GET'])
@requires_student_auth
def get_tags(student):
    tags = TagsFinder.get_all()
    tags_names = []

    for tag in tags:
        tags_names.append(tag.name)

    return jsonify(tags_names), 200


@bp.route('/add-tags', methods=['POST'])
@requires_student_auth
def add_tags(student):
    try:
        tags = request.get_json()["tags"]
    except KeyError:
        return APIErrorValue('Invalid tag').json(500)

    for tag in tags:
        tag = TagsFinder.get_by_name(tag)
        if(tag is None or tag in student.tags):
            continue

        TagsHandler.add_student_tag(student, tag)

    return StudentsValue(student, details=True).json(200)

@bp.route('/delete-tag', methods=['POST'])
@requires_student_auth
def delete_tag(student):
    try:
        tag = request.get_json()["tag"]
    except KeyError:
        return APIErrorValue('Invalid tag').json(500)

    tag = TagsFinder.get_by_name(tag)
    if(tag is None):
        return APIErrorValue('Tag not found').json(404)

    student_tag = TagsFinder.get_student_tag(student, tag)
    if(student_tag is None):
        return APIErrorValue('Student tag not found').json(404)
    
    TagsHandler.delete_student_tag_service(student_tag)

    return StudentsValue(student, details=True).json(200)

@bp.route('/partners', methods=['GET'])
@requires_student_auth
def get_partners(student):
    companies = CompaniesFinder.get_chat_companies({'partnership_tier':'main_sponsor'})
    companies = companies + CompaniesFinder.get_chat_companies({'partnership_tier':'gold'})
    companies = companies + CompaniesFinder.get_chat_companies({'partnership_tier':'silver'})
    companies = companies + CompaniesFinder.get_chat_companies({'partnership_tier':'bronze'})

    return CompaniesValue(companies, False).json(200)

@bp.route('/partner', methods=['GET'])
@requires_student_auth
def get_partner(student):
    name = request.args.get('name', None)
    if name is None:
        return APIErrorValue("Invalid name").json(500)

    company = CompaniesFinder.get_from_name(name)
    if company is None:
        return APIErrorValue('Company not found').json(404)

    return PartnersValue(company, student).json(200)

@bp.route('/companies', methods=['GET'])
@requires_student_auth
def get_companies(student):
    company_names = []
    companies = CompaniesFinder.get_companies_from_default_event()

    for company in companies:
        company_names.append(company.name)

    return jsonify(company_names), 200

@bp.route('/add-companies', methods=['POST'])
@requires_student_auth
def add_companies(student):
    try:
        companies = request.get_json()["companies"]
    except KeyError:
        return APIErrorValue('Invalid company').json(500)

    for company in companies:
        company = CompaniesFinder.get_from_name(company)
        if(company is None or company in student.companies):
            continue

        StudentsHandler.add_student_company(student, company)

    return StudentsValue(student, details=True).json(200)

@bp.route('/delete-company', methods=['POST'])
@requires_student_auth
def delete_company(student):
    try:
        company = request.get_json()["company"]
    except KeyError:
        return APIErrorValue('Invalid company').json(500)

    company = CompaniesFinder.get_from_name(company)
    if(company is None):
        return APIErrorValue('Company not found').json(404)

    student_company = StudentsFinder.get_student_company(student, company)
    if(student_company is None):
        return APIErrorValue('Student company not found').json(404)
    
    StudentsHandler.delete_student_company(student_company)

    return StudentsValue(student, details=True).json(200)

@bp.route('/students-ranking', methods=['GET'])
@requires_student_auth
def get_students_ranking(student):
    students = StudentsFinder.get_top()

    return StudentsValue(students, details=False).json(200)

@bp.route('/squads-ranking', methods=['GET'])
@requires_student_auth
def get_squads_ranking(student):
    squads = SquadsFinder.get_top()

    return SquadsValue(squads).json(200)

@bp.route('/today-squad-reward', methods=['GET'])
@requires_student_auth
def get_today_squad_reward(student):
    now = datetime.utcnow().strftime('%d %b %Y, %a')
    
    squad_reward = RewardsFinder.get_squad_reward_from_date(now)

    if(squad_reward is None):
        return RewardsValue(None).json(200)

    return RewardsValue(squad_reward.reward).json(200)

@bp.route('/squads-rewards', methods=['GET'])
@requires_student_auth
def get_squads_rewards(student):
    squads_rewards = RewardsFinder.get_all_squad_rewards()

    return SquadsRewardsValue(squads_rewards, student.squad).json(200)

@bp.route('/jeecpot-rewards', methods=['GET'])
@requires_student_auth
def get_jeecpot_rewards(student):
    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    return JeecpotRewardsValue(jeecpot_rewards[0], student).json(200)

@bp.route('/chat-token', methods=['GET'])
@requires_student_auth
def get_chat_token(student):
    token = UsersHandler.get_chat_user_token(student.user)

    if token:
        return jsonify({'token':token}), 200
    else:
        return APIErrorValue("Error getting token").json(500)

@bp.route('/chat-room', methods=['GET'])
@requires_student_auth
def get_chat_room(student):
    company_name = request.args.get('company', None)
    user_id = request.args.get('member', None)

    if company_name:
        company = CompaniesFinder.get_from_name(company_name)
        if company is None:
            return APIErrorValue("Company not found").json(404)

        result = UsersHandler.join_channel(student.user, company.chat_id, company.chat_code)
        if result:
            return jsonify({'result':True}), 200
        else:
            return APIErrorValue("Failed to join room").json(500)

    elif user_id:
        company_user = UsersFinder.get_from_external_id(user_id)
        if company_user is None and not company_user.role.name == 'company':
            return APIErrorValue("Invalid user").json(500)
        
        room_id = UsersHandler.create_direct_message(student.user, company_user)
        if room_id is None:
            return APIErrorValue("Failed to create direct message session").json(500)

        return jsonify({"room_id":room_id}), 200

    else:
        return APIErrorValue("No room found").json(404)

@bp.route('/notifications', methods=['GET'])
@requires_student_auth
def get_notifications(student):
    notifications={}

    if(student.squad):
        notifications['squad_xp'] = student.squad.total_points
    
    notifications['invites'] = []
    invitations = SquadsFinder.get_invitations_from_parameters({"receiver_id": student.id})
    for invitation in invitations:
        sender = StudentsFinder.get_from_id(invitation.sender_id)
        notifications['invites'].append(sender.user.name)
    
    notifications['activities'] = []
    activities = ActivitiesFinder.get_next_activity()
    for activity in activities:
        notifications['activities'].append(activity.name)

    return jsonify(notifications), 200