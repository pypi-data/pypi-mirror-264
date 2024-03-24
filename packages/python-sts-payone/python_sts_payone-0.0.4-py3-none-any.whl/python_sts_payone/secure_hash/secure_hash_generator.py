from hashlib import sha256
from collections import OrderedDict


class SecureHashGenerator:
    def __init__(self, auth_token: str, params: dict):
        self.auth_token: str = auth_token

        """The params need to be ordered in alphabetical order"""
        self.params: OrderedDict = OrderedDict(sorted(params.items()))
        print('PARAMS: {}'.format(self.params))

    def make_secure_hash_input_string(self) -> str:
        joined_param_values: str = ''
        for value in self.params.values():
            joined_param_values += str(value).replace(' ', '+')

        print('JOINED PARAMS: {}'.format(joined_param_values))

        return self.auth_token + joined_param_values
    
    def generate_secure_hash(self) -> str:
        input_string: str = self.make_secure_hash_input_string()
        secure_hash: str = sha256(input_string.encode('utf-8')).hexdigest()
        return secure_hash
    
def get_secure_hash(auth_token: str, params: dict) -> str:
    return SecureHashGenerator(auth_token, params).generate_secure_hash()