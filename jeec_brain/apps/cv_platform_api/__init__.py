from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("cv_platform_api_bp", __name__)

from .companies import routes
from .students import routes

import logging

logger = logging.getLogger(__name__)


@bp.route("/")
@bp.route("/index", methods=["GET"])
def index():
    return render_template("cv_platform/index.html")


@bp.route("/index", methods=["POST"])
def choose_role():
    if request.form["submit"] == "Student":
        return redirect(url_for("cv_platform_api_bp.login_student"))

    elif request.form["submit"] == "Company":
        return redirect(url_for("cv_platform_api_bp.login_company"))

    return redirect(url_for("cv_platform_api_bp.index"))
