from flask import Blueprint

bp = Blueprint('students_api', __name__)

from jeec_brain.apps.students_api import routes
from jeec_brain.apps.students_api.resume import routes
