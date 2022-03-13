from config import Config
import fenixedu
import logging

logger = logging.getLogger(__name__)


class CreateTecnicoClientService(object):
    @classmethod
    def __init__(self, fenix_config_file):
        self.fenix_config_file = fenix_config_file

    def call(self):
        try:
            config = fenixedu.FenixEduConfiguration.fromConfigFile(
                self.fenix_config_file
            )
            client = fenixedu.FenixEduClient(config)
            return client
        except Exception as e:
            logger.error(e)
