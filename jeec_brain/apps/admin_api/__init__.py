from flask import Blueprint

bp = Blueprint('admin_api', __name__)

from jeec_brain.apps.admin_api import routes
from jeec_brain.apps.admin_api.companies import routes
from jeec_brain.apps.admin_api.activities import routes
from jeec_brain.apps.admin_api.speakers import routes
from jeec_brain.apps.admin_api.team import routes
from jeec_brain.apps.admin_api.users import routes
from jeec_brain.apps.admin_api.auctions import routes
