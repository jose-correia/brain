#from flask import Blueprint
from flask_openapi3 import APIBlueprint, Tag

#bp = Blueprint('admin_api', __name__)
tag = Tag(name='Admin API', description='Admin side api')
bp = APIBlueprint('admin_api', __name__, url_prefix='/admin', abp_tags=[tag])

from jeec_brain.apps.admin_api import routes
from jeec_brain.apps.admin_api.companies import routes
from jeec_brain.apps.admin_api.activities import routes
from jeec_brain.apps.admin_api.meals import routes
from jeec_brain.apps.admin_api.speakers import routes
from jeec_brain.apps.admin_api.team import routes
from jeec_brain.apps.admin_api.users import routes
from jeec_brain.apps.admin_api.auctions import routes
from jeec_brain.apps.admin_api.events import routes
from jeec_brain.apps.admin_api.student_app import routes