from . import bp
from flask import (
    current_app,
    request,
    redirect,
    jsonify,
)
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
from jeec_brain.values.squad_members_value import SquadMembersValue
from jeec_brain.values.squad_invitations_sent_value import SquadInvitationsSentValue
from jeec_brain.values.squad_invitations_value import SquadInvitationsValue
from jeec_brain.values.student_activities_value import StudentActivitiesValue
from jeec_brain.values.student_event_info_value import StudentEventInfoValue
from jeec_brain.values.rewards_value import RewardsValue
from jeec_brain.values.squads_rewards_value import SquadsRewardsValue
from jeec_brain.values.jeecpot_rewards_value import JeecpotRewardsValue
from jeec_brain.values.levels_value import LevelsValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.values.partners_value import PartnersValue

from jeec_brain.apps.auth.wrappers import requires_student_auth

from jeec_brain.schemas.student_api.schemas import *

# Login routes
@bp.get("/login")
def login_student():
    """Login page
    Login url used to redirect to fenix login.
    <b>Returns:</b>
        REDIRECT: Redirect to URL of the redirect page (/redirect_uri)
    """
    return AuthHandler.redirect_to_fenix_login()


@bp.route("/redirect_uri")
def redirect_uri():
    """Refirect uri after fenix login
    Refirect uri returned after fenix login from the definitions of the app in fenix
    <b>Returns:</b>
        REDIRECT: Redirects to the default jeec website (if user is correctly validated adds token in url)
    """
    if request.args.get("error") == "access_denied":
        return redirect(Config.STUDENT_APP_URL)

    fenix_auth_code = request.args.get("code")

    student, encrypted_jwt = AuthHandler.login_student(fenix_auth_code)

    if student:
        return redirect(Config.STUDENT_APP_URL + "?token=" + encrypted_jwt)

    else:
        return redirect(Config.STUDENT_APP_URL)


@bp.get("/info", responses={"200": StudentInfoList})
@requires_student_auth
def get_info(student):
    """Get information on Student
    Retrieve the information related to the current logged in student
    <b>Returns:</b>
        StudentsValue: Information about the current user (more information with details = True)
    """
    return StudentsValue(student, details=True).json(200)


@bp.get("/today-login", responses={"200": StudentInfoList, "409": APIError})
@requires_student_auth
def today_login(student):
    """Register current student's day login
    Register the today's login for the current logged in student

    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    now = datetime.utcnow()
    date = now.strftime("%d %b %Y, %a")
    event = EventsFinder.get_default_event()
    dates = EventsHandler.get_event_dates(event)

    if date in dates:
        student_login = StudentsFinder.get_student_login(student, date)
        if student_login is None:
            StudentsHandler.add_student_login(student, date)
            StudentsHandler.add_points(student, int(Config.REWARD_LOGIN))
        else:
            return APIErrorValue("Already loggedin today").json(409)
    else:
        return APIErrorValue("Date out of event").json(409)

    return StudentsValue(student, details=True).json(200)


@bp.get("/students", responses={"200": StudentInfoList})
@requires_student_auth
def get_students(student, query: SearchQuery):
    """Get list of students according to filters
    Retrieve the student list according to the search query, the students internal or external id
    <b>Args:</b>
        query (SearchQuery): Optional string to look for
    <b>Returns:</b>
        StudentsValue: Information about the current user (more information with details = True)
    """
    search = query.search

    students = StudentsFinder.get_from_search_without_student(
        search, student.external_id
    )

    return StudentsValue(students, details=False).json(200)


@bp.get("/levels", responses={"200": LevelDetailList})
@requires_student_auth
def get_levels(student):
    """Check all the levels
    Returns a list with all the levels and their intervals
    <b>Returns:</b>
        LevelsValue: List of all levels available
    """
    levels = LevelsFinder.get_all_levels()

    return LevelsValue(levels, True).json(200)


@bp.get("/squad", responses={"200": SquadDetailList, "409": APIError})
@requires_student_auth
def get_squad(student):
    """Get squad of the current user
    Retrieve the information about the current user squad
    <b>Returns:</b>
    IF user has a squad: -> SquadDetailList: List of all squads and their details
    IF user doesn't have a squad: -> An error message and an error code.
    """
    if student.squad is None:
        return APIErrorValue("No squad found").json(404)

    return SquadsValue(student.squad).json(200)


@bp.post("/squad", responses={"200": SquadDetailList, "401": APIError, "500": APIError})
@requires_student_auth
def create_squad(student, form: CreateSquad):  # , body:PhotoInput):
    """Create a squad for current user
    Create a squad for the current user using the chosen values
    <b>Args:</b>
    form (CreateSquad): form with the name and cry of the squad
    body (FileInput): contains the file for the squad photo
    <b>Returns:</b>
    IF a squad is created: -> SquadDetailList: List of all squads and their details
    IF there is an error: -> An error message and an error code.
    """
    if student.squad is not None:
        return APIErrorValue("Student already has squad").json(401)

    name = form.name
    cry = form.cry
    # file = body.photo

    if name is None or cry is None:
        return APIErrorValue("Invalid squad info").json(500)

    if "file" not in request.files:
        return APIErrorValue("No image detected").json(500)

    file = request.files["file"]

    if file and file.filename != "":
        squad = SquadsHandler.create_squad(
            name=name, cry=cry, captain_ist_id=student.user.username
        )
        if squad is None:
            return APIErrorValue("Error creating squad").json(500)

        result, msg = SquadsHandler.upload_squad_image(file, str(squad.external_id))
        if not result:
            SquadsHandler.delete_squad(squad)
            return APIErrorValue(msg).json(500)

        StudentsHandler.add_squad_member(student, squad)
    else:
        return APIErrorValue("No image found").json(500)

    return SquadsValue(squad).json(200)


@bp.post(
    "/invite-squad",
    responses={"200": SuccessResponse, "401": APIError, "500": APIError},
)
@requires_student_auth
def invite_squad(student, body: MemberList):
    """Invite students into the squad of the current user
    Send invites to the students for the current users squad
    <b>Returns:</b>
    IF invite is successful: -> Success message.
    IF there is an error: -> An error message and an error code.
    """
    if student.squad is None:
        return APIErrorValue("No squad found").json(401)

    try:
        members = body.members
        # members = request.get_json()["members"]
    except KeyError:
        return APIErrorValue("Invalid members").json(500)

    if StudentsHandler.invite_squad_members(student, members):
        return jsonify("Success"), 200
    else:
        return APIErrorValue("Failed to invite").json(500)


@bp.post(
    "/cancel-invitation",
    responses={"200": SuccessResponse, "404": APIError, "500": APIError},
)
@requires_student_auth
def cancel_invite(student, body: Invitation):
    """Cancels invitation of students into the squad of the current user
    <b>Returns:</b>
    IF invite is canceled: -> Success message.
    IF there is an error: -> An error message and an error code.
    """
    # try:
    #     receiver_id = request.get_json()["id"]
    # except KeyError:
    #     return APIErrorValue('Invalid members').json(500)

    receiver_id = body.id
    if receiver_id is None:
        return APIErrorValue("Invalid members").json(500)

    invitations = SquadsFinder.get_invitations_from_parameters(
        {"sender_id": student.id, "receiver_id": receiver_id}
    )
    if invitations is None or len(invitations) == 0:
        return APIErrorValue("No invites found").json(404)

    for invitation in invitations:
        SquadsHandler.delete_squad_invitation(invitation)

    return jsonify("Success"), 200


@bp.get("/squad-invitations-received", responses={"200": SquadInvitationsReceivedList})
@requires_student_auth
def get_squad_invitations_received(student):
    """Check list of invitations received
    Retrieves a list of the invitations received
    <b>Returns:</b>
        SquadInvitationsReceivedList: List containing all the squad invitations received by the current user
    """
    invitations = SquadsFinder.get_invitations_from_parameters(
        {"receiver_id": student.id}
    )

    return SquadInvitationsValue(invitations).json(200)


@bp.get("/squad-invitations-sent", responses={"200": SquadInvitationsSentList})
@requires_student_auth
def get_squad_invitations_sent(student):
    """Check list of invitations sent
    Retrieves a list of the invitations sent
    <b>Returns:</b>
        SquadInvitationssentList: List containing all the squad invitations sent by the current user
    """
    invitations = SquadsFinder.get_invitations_from_parameters(
        {"sender_id": student.id}
    )

    return SquadInvitationsSentValue(
        [invitation.receiver for invitation in invitations]
    ).json(200)


@bp.post(
    "/accept-invitation",
    responses={"200": StudentInfoList, "404": APIError, "500": APIError},
)
@requires_student_auth
def accept_invitation(student, body: Invitation_external):
    """Accept an invitation for the current student
    Accept an invitation for a squad that was sent to the current student
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     invitation_id = request.get_json()["invitation_id"]
    # except KeyError:
    #     return APIErrorValue('Invalid invitation').json(500)

    if body.invitation_id is None:
        return APIErrorValue("Invalid invitation").json(500)

    invitation_id = body.invitation_id

    invitation = SquadsFinder.get_invitation_from_external_id(invitation_id)
    if invitation is None:
        return APIErrorValue("Invitation not found").json(404)

    student = StudentsHandler.accept_invitation(student, invitation)
    if not student:
        return APIErrorValue("Failed to join squad").json(500)

    return StudentsValue(student, details=True).json(200)


@bp.post(
    "reject-invitation",
    responses={"200": StudentInfoList, "404": APIError, "500": APIError},
)
@requires_student_auth
def reject_invitation(student, body: Invitation_external):
    """Reject an invitation for the current student
    Reject an invitation for a squad that was sent to the current student
    <b>Returns:</b>
        On Success: -> A success message is sent.
        On Error: -> An error message and error code.
    """
    # try:
    #     invitation_id = request.get_json()["invitation_id"]
    # except KeyError:
    #     return APIErrorValue('Invalid invitation').json(500)

    if body.invitation_id is None:
        return APIErrorValue("Invalid invitation").json(500)

    invitation_id = body.invitation_id

    invitation = SquadsFinder.get_invitation_from_external_id(invitation_id)
    if invitation is None:
        return APIErrorValue("Invitation not found").json(404)

    SquadsHandler.delete_squad_invitation(invitation)

    return jsonify("Success"), 200


@bp.post("leave-squad", responses={"200": StudentInfoList})
@requires_student_auth
def leave_squad(student):
    """Leave current student's squad
    Make current student leave the squad he is in
    <b>Returns:</b>
        StudentsValue: Information about the current user (more information with details = True)
    """
    student = StudentsHandler.leave_squad(student)

    return StudentsValue(student, details=True).json(200)


@bp.post(
    "kick-member",
    responses={
        "200": StudentInfoList,
        "401": APIError,
        "404": APIError,
        "500": APIError,
    },
)
@requires_student_auth
def kick_member(student, body: Member):
    """Kick a member from the current student's squad
    If the current user is the squad captain kick the chosen member off the squad
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    if not student.is_captain():
        return APIErrorValue("Student is not captain").json(401)

    # try:
    #     member_ist_id = request.get_json()["ist_id"]
    # except KeyError:
    #     return APIErrorValue('Invalid IST id').json(500)

    if body.ist_id is None:
        return APIErrorValue("Invalid IST id").json(500)

    member_ist_id = body.ist_id

    member = StudentsFinder.get_from_ist_id(member_ist_id)
    if member is None:
        return APIErrorValue("Member not found").json(404)

    StudentsHandler.leave_squad(member)

    return SquadsValue(student.squad).json(200)


@bp.post("/redeem-code", responses={"200": StudentInfoList, "500": APIError})
@requires_student_auth
def redeem_code(student):  # , body:ReferralCode):
    """Redeem an inserted code
    Redeem the inserted code for the current student

    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    try:
        code = request.get_json()["code"].replace("-", "")
    except KeyError:
        return APIErrorValue("Code not inserted").json(500)

    # return APIErrorValue("Code submission closed").json(500)

    error_msg, student = ActivityCodesHandler.redeem_activity_code(student, code)
    if(error_msg == "Code not found"):
        redeemed_student = StudentsFinder.get_from_referral_code(code)
        if(not redeemed_student or redeemed_student.id == student.id):
            return APIErrorValue('Invalid code').json(500)

        error_msg, student = StudentsHandler.redeem_referral(student, redeemed_student, code)
        if error_msg:
            return APIErrorValue(error_msg).json(500)

    elif(error_msg):
        return APIErrorValue(error_msg).json(500)

    return StudentsValue(student, details=True).json(200)


@bp.get("/activities", responses={"200": ActivityList})
@requires_student_auth
def get_activities(student, query: DateQuery):
    """Check activity list
    Retrieves a list with the activities
    <b>Returns:</b>
        StudentActivitiesValue: List of the activities
    """
    event = EventsFinder.get_default_event()
    # date = request.args.get('date', None)
    date = query.date

    if date is None:
        activities = event.activities
    else:
        activities = ActivitiesFinder.get_from_parameters(
            {"event_id": event.id, "day": date}
        )

    return StudentActivitiesValue(activities, student).json(200)


@bp.get("/quests", responses={"200": ActivityList})
@requires_student_auth
def get_quests(student):
    """Check quest list
    Retrieves a list with the quests
    <b>Returns:</b>
        StudentActivitiesValue: List of the quests
    """
    activities = ActivitiesFinder.get_quests()

    return StudentActivitiesValue(activities, student, True).json(200)


@bp.get("/event-dates", responses={"200": SuccessResponse})
@requires_student_auth
def get_activity_dates(student):
    """Check event list
    Retrieves a list with the event dates
    <b>Returns:</b>
        Json: List of all event dates
    """
    event = EventsFinder.get_default_event()
    dates = EventsHandler.get_event_dates(event)

    return jsonify(dates), 200


@bp.get("/event-info", responses={"200": Event})
@requires_student_auth
def get_event_info(student):
    """Check default event info
    Retrieves the info about the default event
    <b>Returns:</b>
        StudentEventInfoValue: Info about the current event
    """
    event = EventsFinder.get_default_event()

    return StudentEventInfoValue(event).json(200)


@bp.post("/add-linkedin", responses={"200": StudentInfoList, "500": APIError})
@requires_student_auth
def add_linkedin(student, body: UrlInput):
    """Add linkedin url to current student

    <b>Args:</b>
    body (UrlInput): contains the url for the linkedin
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     url = request.get_json()["url"]
    # except KeyError:
    #     return APIErrorValue('Invalid url').json(500)

    url = body.url
    if url is None:
        return APIErrorValue("Invalid url").json(500)

    if not student.linkedin_url:
        StudentsHandler.add_points(student, int(Config.REWARD_LINKEDIN))
    StudentsHandler.update_student(student, linkedin_url=url)

    return StudentsValue(student, details=True).json(200)


@bp.post("/add-cv", responses={"200": StudentInfoList, "500": APIError})
@requires_student_auth
def add_cv(student):
    """Add cv to current student
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    if "cv" not in request.files:
        return APIErrorValue("No cv found").json(500)

    file = request.files["cv"]
    if file.filename == "":
        return APIErrorValue("No cv found").json(500)

    if file and FileHandler.allowed_file(file.filename):
        filename = "cv-" + student.user.username + ".pdf"

        if not FileHandler.upload_file(file, filename):
            return APIErrorValue("Error uploading file").json(500)

        if not student.uploaded_cv:
            StudentsHandler.update_student(student, uploaded_cv=True)
            StudentsHandler.add_points(student, int(Config.REWARD_CV))

    else:
        return APIErrorValue("Wrong file extension").json(500)

    return StudentsValue(student, details=True).json(200)


@bp.get("/cv", responses={"200": SuccessResponse, "500": APIError})
@requires_student_auth
def get_cv(student):
    """Retrieve the current student's cv
    <b>Returns:</b>
        Json: Returns the current student's cv in json
    """
    if not student.uploaded_cv:
        return APIErrorValue("No CV uploaded").json(404)

    filename = "cv-" + student.user.username + ".pdf"

    with open(
        os.path.join(current_app.root_path, "storage", filename), mode="rb"
    ) as file:
        fileContent = file.read()

    return jsonify(
        {
            "data": str(base64.b64encode(fileContent), "utf-8"),
            "content-type": "application/pdf",
        }
    )


@bp.get("/tags", responses={"200": SuccessResponse})
@requires_student_auth
def get_tags(student):
    """Check all tags
    Check all tags created on the database
    <b>Returns:</b>
        Json: Returns the list of tags available on the database
    """
    tags = TagsFinder.get_all()
    tags_names = []

    for tag in tags:
        tags_names.append(tag.name)

    return jsonify(tags_names), 200


@bp.post("/add-tags", responses={"200": StudentInfoList, "500": APIError})
@requires_student_auth
def add_tags(student, body: TagsInput):
    """Adds tags to the current student
    <b>Args:</b>
    body (SearchQuery): contains the list of tags to add
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     tags = request.get_json()["tags"]
    # except KeyError:
    #     return APIErrorValue('Invalid tag').json(500)

    tags = body.tags
    if tags is None:
        return APIErrorValue("Invalid tag").json(500)

    for tag in tags:
        tag = TagsFinder.get_by_name(tag)
        if tag is None or tag in student.tags:
            continue

        TagsHandler.add_student_tag(student, tag)

    return StudentsValue(student, details=True).json(200)


@bp.post(
    "/delete-tag", responses={"200": StudentInfoList, "404": APIError, "500": APIError}
)
@requires_student_auth
def delete_tag(student, body: TagDelete):
    """Deletes tags from the current student
    <b>Args:</b>
    body (SearchQuery): contains the list of tags to delete
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     tag = request.get_json()["tag"]
    # except KeyError:
    #     return APIErrorValue('Invalid tag').json(500)

    tag = body.tag
    if tag is None:
        return APIErrorValue("Invalid tag").json(500)

    tag = TagsFinder.get_by_name(tag)
    if tag is None:
        return APIErrorValue("Tag not found").json(404)

    student_tag = TagsFinder.get_student_tag(student, tag)
    if student_tag is None:
        return APIErrorValue("Student tag not found").json(404)

    TagsHandler.delete_student_tag_service(student_tag)

    return StudentsValue(student, details=True).json(200)


@bp.get("/partners", responses={"200": CompaniesList})
@requires_student_auth
def get_partners(student):
    """Retrieve full list of partners
    <b>Returns:</b>
        CompaniesValue: contains the full list of partners

    """
    companies = CompaniesFinder.get_chat_companies({"partnership_tier": "main_sponsor"})
    companies = companies + CompaniesFinder.get_chat_companies(
        {"partnership_tier": "gold"}
    )
    companies = companies + CompaniesFinder.get_chat_companies(
        {"partnership_tier": "silver"}
    )
    companies = companies + CompaniesFinder.get_chat_companies(
        {"partnership_tier": "bronze"}
    )
    print(companies)
    return CompaniesValue(companies, False).json(200)


@bp.get("/partner", responses={"200": PartnerCompany, "404": APIError, "500": APIError})
@requires_student_auth
def get_partner(student, query: PartnerName):
    """Searches for specific partner company
    <b>Args:</b>
        query (PartnerName): Company to look for
    <b>Returns:</b>
        PartnersValue: List with all the user from a chosen company
    """
    # name = request.args.get('name', None)
    name = query.name
    if name is None:
        return APIErrorValue("Invalid name").json(500)

    company = CompaniesFinder.get_from_name(name)
    if company is None:
        return APIErrorValue("Company not found").json(404)

    return PartnersValue(company, student).json(200)


@bp.get("/companies", responses={"200": SuccessResponse})
@requires_student_auth
def get_companies(student):
    """Retrieve the company list from the default event
    <b>Returns:</b>
        Json: Returns the company list from the default event
    """
    company_names = []
    companies = CompaniesFinder.get_companies_from_default_event()

    for company in companies:
        company_names.append(company.name)

    return jsonify(company_names), 200


@bp.post(
    "/add-companies",
    responses={"200": StudentInfoList, "404": APIError, "500": APIError},
)
@requires_student_auth
def add_companies(student, body: Companylist):
    """Add the list of companies to the current user
    <b>Args:</b>
        body (Companylist): List of companies to add to the current user
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     companies = request.get_json()["companies"]
    # except KeyError:
    #     return APIErrorValue('Invalid company').json(500)

    companies = body.companies
    if companies is None:
        return APIErrorValue("Invalid company").json(500)

    for company in companies:
        company = CompaniesFinder.get_from_name(company)
        if company is None or company in student.companies:
            continue

        StudentsHandler.add_student_company(student, company)

    return StudentsValue(student, details=True).json(200)


@bp.post(
    "/delete-company",
    responses={"200": StudentInfoList, "404": APIError, "500": APIError},
)
@requires_student_auth
def delete_company(student, body: CompanyName):
    """Delete company from current student's company list
    <b>Args:</b>
        body (CompanyName): List of companies to add to the current user
    <b>Returns:</b>
        On Success: -> StudentsValue: Information about the current user (more information with details = True)
        On Error: -> An error message and error code.
    """
    # try:
    #     company = request.get_json()["company"]
    # except KeyError:
    #     return APIErrorValue('Invalid company').json(500)

    company = body.company
    if company is None:
        return APIErrorValue("Invalid company").json(500)

    company = CompaniesFinder.get_from_name(company)
    if company is None:
        return APIErrorValue("Company not found").json(404)

    student_company = StudentsFinder.get_student_company(student, company)
    if student_company is None:
        return APIErrorValue("Student company not found").json(404)

    StudentsHandler.delete_student_company(student_company)

    return StudentsValue(student, details=True).json(200)


@bp.get("/students-ranking", responses={"200": StudentInfoList})
@requires_student_auth
def get_students_ranking(student):
    """Get current top 20 students in the rankings
    <b>Returns:</b>
        StudentsValue: Information about the users (more information with details = True)
    """
    students = StudentsFinder.get_top(20)

    return StudentsValue(students, details=False).json(200)


@bp.get("/squads-ranking", responses={"200": SquadDetailList})
@requires_student_auth
def get_squads_ranking(student):
    """Get current top 10 squads in the rankings
    <b>Returns:</b>
        SquadsValue: Information about the squad
    """
    squads = SquadsFinder.get_top()

    return SquadsValue(squads).json(200)


@bp.get("/daily-squads-ranking", responses={"200": SquadDetailList})
@requires_student_auth
def get_daily_squads_ranking(student):
    """Get current top 10 squads in the daily rankings
    <b>Returns:</b>
        SquadsValue: Information about the squad
    """
    squads = SquadsFinder.get_daily_top()

    return SquadsValue(squads).json(200)


@bp.get("/today-squad-reward", responses={"200": Rewards})
@requires_student_auth
def get_today_squad_reward(student):
    """Get the todays squad reward
    <b>Returns:</b>
        RewardsValue: Information about the reward
    """
    now = datetime.utcnow().strftime("%d %b %Y, %a")

    squad_reward = RewardsFinder.get_squad_reward_from_date(now)

    if squad_reward is None:
        return RewardsValue(None).json(200)

    return RewardsValue(squad_reward.reward).json(200)


@bp.get("/squads-rewards", responses={"200": SquadRewardsList})
@requires_student_auth
def get_squads_rewards(student):
    """Get all squad rewards
    <b>Returns:</b>
        SquadsRewardsValue: Information about all squad rewards
    """
    squads_rewards = RewardsFinder.get_all_squad_rewards()

    return SquadsRewardsValue(squads_rewards, student.squad).json(200)


@bp.get("/jeecpot-rewards", responses={"200": JeecpotRewards})
@requires_student_auth
def get_jeecpot_rewards(student):
    """Retrieve the jeecpot rewards for the current student
    <b>Returns:</b>
        JeecpotRewardsValue: Returns list with the jeecpot rewards for the current student
    """
    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    return JeecpotRewardsValue(jeecpot_rewards[0], student).json(200)


@bp.get("/chat-token", responses={"200": SuccessResponse, "500": APIError})
@requires_student_auth
def get_chat_token(student):
    """Get chat token for the current student
    <b>Returns:</b>
        On Success: -> Json: Json with the token.
        On Error: -> An error message and error code.
    """
    token = UsersHandler.get_chat_user_token(student.user)

    if token:
        return jsonify({"token": token}), 200
    else:
        return APIErrorValue("Error getting token").json(500)


@bp.get(
    "/chat-room", responses={"200": SuccessResponse, "404": APIError, "500": APIError}
)
@requires_student_auth
def get_chat_room(student, query: CompanyChatRoom):
    """Join a company's chat room

    <b>Args:</b>
        query (CompanyChatRoom): Query with the company's name or a company user's user_id
    <h3>If join by company</h3>
    <b>Returns:</b>
        On Success: -> Json: Json with result True.
        On Error: -> An error message and error code.

    <h3>If join by company user</h3>
    <b>Returns:</b>
        On Success: -> Json: Json with the chat room id.
        On Error: -> An error message and error code.
    """
    # company_name = request.args.get('company', None)
    # user_id = request.args.get('member', None)
    company_name = query.company
    user_id = query.member

    if company_name:
        company = CompaniesFinder.get_from_name(company_name)
        if company is None:
            return APIErrorValue("Company not found").json(404)

        result = UsersHandler.join_channel(
            student.user, company.chat_id, company.chat_code
        )
        if result:
            return jsonify({"result": True}), 200
        else:
            return APIErrorValue("Failed to join room").json(500)

    elif user_id:
        company_user = UsersFinder.get_from_external_id(user_id)
        if company_user is None and not company_user.role.name == "company":
            return APIErrorValue("Invalid user").json(500)

        room_id = UsersHandler.create_direct_message(student.user, company_user)
        if room_id is None:
            return APIErrorValue("Failed to create direct message session").json(500)

        return jsonify({"room_id": room_id}), 200

    else:
        return APIErrorValue("No room found").json(404)


@bp.get("/notifications", responses={"200": SuccessResponse})
@requires_student_auth
def get_notifications(student):
    """Retrieve the list of notifications for current user
    Retrieve a list of notifications containing information on the squad xp, invitations and activities
    <b>Returns:</b>
        On Success: -> Json: Json with the notifications.
        On Error: -> An error message and error code.
    """
    notifications = {}

    if student.squad:
        notifications["squad_xp"] = student.squad.total_points

    notifications["invites"] = []
    invitations = SquadsFinder.get_invitations_from_parameters(
        {"receiver_id": student.id}
    )
    for invitation in invitations:
        sender = StudentsFinder.get_from_id(invitation.sender_id)
        notifications["invites"].append(sender.user.name)

    notifications["activities"] = []
    activities = ActivitiesFinder.get_next_activity()
    for activity in activities:
        notifications["activities"].append(activity.name)

    return jsonify(notifications), 200
