from flask import Blueprint, request, redirect, url_for

bp = Blueprint('auth_api', __name__)

# setup Tecnico Cliente for Fenix Auth
from .handlers.tecnico_client_handler import TecnicoClientHandler

fenix_config_file = 'fenixedu.ini'
fenix_client = TecnicoClientHandler.create_client(fenix_config_file=fenix_config_file)
