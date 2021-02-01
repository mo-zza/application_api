from dataclasses import asdict

from src.application.dto.users_dto import PasswordDto
from src.domain.value.collection import userPrivateCol

class PasswordDomainService:
    def __init__(self, uid, simple_pw):
        self.uid = uid
        self.simple_pw = simple_pw

    def change_password(self):
        params = PasswordDto(self.simple_pw)
        return asdict(params)
        