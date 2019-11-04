import secrets
import string


class GenerateCredentialsService():

    def call(self) -> bool:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        
        return password
        