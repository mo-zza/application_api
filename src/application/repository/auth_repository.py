from src import firestore
from src.domain.value.exceptions import UnAuthenticationError


class AuthRepo:
    def __init__(self, user_email: str, token: str = None) -> None:
        self.firestore  = firestore
        self.user_email = user_email
        if token != None:
            self.token = token
    
    def find_uid(self):
        try:
            uid = self.firestore.get_auth_user(self.user_email).uid
        except:
            raise UnAuthenticationError
        return uid