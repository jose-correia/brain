from flask import Blueprint

bp = Blueprint('admin_api', __name__)

from . import routes
