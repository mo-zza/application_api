from src.infrastructure.token import JwtToken
from src.domain.value.exceptions import VerifyPassword
from src.infrastructure.multi_thread import ThreadProcess


class SignInDomainService:
    def __init__(self, uid):
        self.uid = uid

    def get_token(self, req_simple_pw, simple_pw):
        if req_simple_pw != simple_pw:
            raise VerifyPassword
        token = JwtToken().create_token(self.uid)
        return token