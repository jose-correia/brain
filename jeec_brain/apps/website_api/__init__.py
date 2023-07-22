# from flask import Blueprint
from flask_openapi3 import APIBlueprint, Tag

# bp = Blueprint('website_api_bp', __name__)
tag = Tag(name="Website API", description="Website api")
bp = APIBlueprint("website_api_bp", __name__, url_prefix="/website", abp_tags=[tag])

from . import routes
