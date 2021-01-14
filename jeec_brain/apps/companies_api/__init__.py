from flask import Blueprint

bp = Blueprint('companies_api', __name__)

from jeec_brain.apps.companies_api import routes
from jeec_brain.apps.companies_api.auctions import routes
from jeec_brain.apps.companies_api.activities import routes
from jeec_brain.apps.companies_api.meals import routes
from jeec_brain.apps.companies_api.resumes import routes
