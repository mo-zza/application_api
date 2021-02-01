from src.application.dto.users_dto import PasswordInputDto, PasswordOutPutDto
from src.domain.services.password_domain_service import PasswordDomainService
from src.application.repository.user_repository import UserRepo
from src.domain.value.data import eventLoop

class PasswordApplicationService:
    def __init__(self, input_dto: PasswordInputDto):
        self._input_dto = input_dto

    def get_password(self): 
        uid       = self._input_dto.uid
        simple_pw = eventLoop.run_until_complete(UserRepo(uid).find_simple_pw())
        return PasswordOutPutDto(simple_pw)

    def change_password(self):
        uid             = self._input_dto.uid
        new_simple_pw   = self._input_dto.simple_pw
        password_params = PasswordDomainService(uid, new_simple_pw).change_password()
        UserRepo(uid).update_simple_pw(password_params)
        return PasswordOutPutDto(new_simple_pw)