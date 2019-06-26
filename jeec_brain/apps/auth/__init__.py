from flask import Blueprint

bp = Blueprint('auth', __name__)

from .handlers.tecnico_client_handler import TecnicoClientHandler
fenix_config_file = 'fenixedu.ini'
client = TecnicoClientHandler.create_client(fenix_config_file=fenix_config_file)
    
from . import routes