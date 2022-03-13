# from flask import Blueprint
from flask_openapi3 import APIBlueprint, Tag

# bp = Blueprint('student_api_bp', __name__)
tag = Tag(name="Students API", description="Student side api")
bp = APIBlueprint("student_api_bp", __name__, url_prefix="/student", abp_tags=[tag])

from . import routes
