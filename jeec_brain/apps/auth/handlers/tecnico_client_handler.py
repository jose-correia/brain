from jeec_brain.apps.auth.services.create_tecnico_client_service import (
    CreateTecnicoClientService,
)


class TecnicoClientHandler(object):
    @staticmethod
    def create_client(fenix_config_file):
        return CreateTecnicoClientService(fenix_config_file=fenix_config_file).call()

    @staticmethod
    def get_authentication_url(client):
        url = client.get_authentication_url()
        return url

    @staticmethod
    def get_user(client, fenix_auth_code):
        user = client.get_user_by_code(fenix_auth_code)
        return user

    @staticmethod
    def get_person(client, user):
        person = client.get_person(user)
        return person
