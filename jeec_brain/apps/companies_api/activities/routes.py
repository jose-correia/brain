from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for, jsonify
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.models.enums.code_flow_enum import CodeFlowEnum
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.companies_api.activities.schemas import *
from datetime import datetime
from config import Config


@bp.get("/activity/<string:activity_external_id>")
@require_company_login
def get_activity_type(company_user, path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue("No activity found").json(404)

    chat_token = UsersHandler.get_chat_user_token(company_user.user)
    chat_url = (
        (Config.ROCKET_CHAT_APP_URL + "home?resumeToken=" + chat_token)
        if chat_token
        else None
    )

    return render_template(
        "companies/activities/activity.html",
        activity=activity,
        chat_url=chat_url,
        error=None,
        user=company_user,
    )


@bp.post("/activity/<string:activity_external_id>/code")
@require_company_login
def generate_code(company_user, path: ActivityPath):
    now = datetime.utcnow()
    today = now.strftime("%d %b %Y, %a")

    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if (
        activity.code_work_flow
        in [CodeFlowEnum.CompanyMultiUseCode, CodeFlowEnum.CompanyOneUseCode]
        and activity.day == today
    ):
        activity_code = ActivityCodesHandler.create_activity_code(
            activity_id=activity.id
        )

        return jsonify(activity_code.code)

    return APIErrorValue("Not allowed").json(401)


@bp.post("/activity/<string:activity_external_id>/istid")
@require_company_login
def use_istid(company_user, path: ActivityPath):
    now = datetime.utcnow()
    today = now.strftime("%d %b %Y, %a")

    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity.code_work_flow in [CodeFlowEnum.CompanyISTID] and activity.day == today:
        ist_id = request.form.get("istid")
        student = StudentsFinder.get_from_ist_id(ist_id)
        if not student:
            return APIErrorValue("Student not found").json(401)

        student_activity = ActivitiesHandler.add_student_activity(
            student, activity, ist_id
        )
        if student_activity:
            StudentsHandler.add_points(student, activity.points)

            return jsonify("Code redeem successfully")

        return APIErrorValue("Failed to redeem code").json(500)

    return APIErrorValue("Not allowed").json(401)
