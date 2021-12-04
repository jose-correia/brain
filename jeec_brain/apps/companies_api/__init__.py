#from flask import Blueprint
from flask_openapi3 import APIBlueprint, Tag

#bp = Blueprint('companies_api', __name__)
tag = Tag(name='Companies API', description='Company side api')
bp = APIBlueprint('companies_api', __name__, url_prefix='/companies', abp_tags=[tag])

from jeec_brain.apps.companies_api import routes
from jeec_brain.apps.companies_api.auctions import routes
from jeec_brain.apps.companies_api.activities import routes
from jeec_brain.apps.companies_api.meals import routes
from jeec_brain.apps.companies_api.resumes import routes
from jeec_brain.apps.companies_api.statistics import routes
