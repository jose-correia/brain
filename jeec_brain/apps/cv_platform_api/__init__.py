from flask import Blueprint

bp = Blueprint('cv_platform_api_bp', __name__)

from . import routes
