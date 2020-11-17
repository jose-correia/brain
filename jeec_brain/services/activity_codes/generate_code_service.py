import secrets
import string


class GenerateCodeService():

    def call(self) -> bool:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(16))
        
        return password
        