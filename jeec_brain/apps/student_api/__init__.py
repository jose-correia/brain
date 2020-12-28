from flask import Blueprint

bp = Blueprint('student_api_bp', __name__)

from . import routes
