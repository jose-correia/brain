from jeec_brain.apps.companies_api import bp
from flask import Response, send_file, render_template, send_from_directory, jsonify, make_response, request
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.schemas.companies_api.resumes.schemas import *
from jeec_brain.finders.companies_finder import CompaniesFinder
from datetime import datetime

import json
from jeec_brain.apps.auth.wrappers import requires_client_auth


@bp.get("/resumes")
@require_company_login
def resumes_dashboard(company_user):
    if company_user.company.cvs_access:
        event = EventsFinder.get_default_event()
        today = datetime.now()
        cvs_access_start = datetime.strptime(event.cvs_access_start, "%d %b %Y, %a")
        cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %b %Y, %a")

        if today < cvs_access_start or today > cvs_access_end:
            return render_template(
                "companies/resumes/resumes_dashboard.html",
                cv_students=None,
                interested_students=None,
                error="Out of access date",
            )
    else:
        return render_template(
            "companies/resumes/resumes_dashboard.html",
            cv_students=None,
            interested_students=None,
            error="Not authorized",
        )

    company_students = StudentsFinder.get_company_students(
        company_user.company, uploaded_cv=True
    )

    return render_template(
        "companies/resumes/resumes_dashboard.html",
        company_students=company_students,
        error=None,
    )


@bp.get("/resumes/<string:student_external_id>/download")
@require_company_login
def download_resume(company_user, path: StudentPath):
    student = StudentsFinder.get_from_external_id(path.student_external_id)
    if student is None:
        return render_template(
            "companies/resumes/resumes_dashboard.html", error="Student not found"
        )

    filename = "cv-" + student.user.username + ".pdf"

    return send_from_directory(directory="storage", filename=filename)


@bp.get("/resumes/download")
@require_company_login
def download_resumes(company_user):
    zip_file = FileHandler.get_files_zip()

    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file, as_attachment=True, attachment_filename="curriculos_JEEC21.zip"
    )


@bp.post("/resumes/vue")
@requires_client_auth
def resumes_dashboard_vue():
    company_name = json.loads(request.data.decode('utf-8'))['company']
    company = CompaniesFinder.get_from_name(company_name)
    if company.cvs_access:
        print("Access")
        event = EventsFinder.get_default_event()
        today = datetime.now()
        cvs_access_start = datetime.strptime(event.cvs_access_start, "%d %b %Y, %a")
        cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %b %Y, %a")
        print(cvs_access_start)
        print(cvs_access_end)

        # if today < cvs_access_start or today > cvs_access_end:
        #     return make_response(jsonify({
        #         "error":"Out of access date",
        #         "company_students": []
        #     }))
        # else:
        company_students = StudentsFinder.get_company_students(
        company, uploaded_cv=True
        )

        return make_response(jsonify({
                    "error":"",
                    "company_students": company_students
                }))
    print("No Access")

    return make_response(jsonify({
                    "error":"Not authorized",
                    "company_students": []
                }))


@bp.get("/resumes/download_vue")
@requires_client_auth
def download_resumes_vue():
    zip_file = FileHandler.get_files_zip()

    if not zip_file:
        return Response(response="Invalid zip file", status="400")

    return send_file(
        zip_file, as_attachment=True, attachment_filename="curriculos_JEEC21.zip"
    )