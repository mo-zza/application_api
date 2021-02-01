from src.domain.entities.users_entity import Users
from src.domain.services.sign_in_domain_service import SignInDomainService
from src.application.dto.users_dto import SignInInputDto, SignInOutputDto
from src.application.repository.user_repository import UserRepo
from src.domain.value.data import eventLoop


class SignApplicationService:
    def __init__(self, input_dto: SignInInputDto):
        self._input_dto = input_dto

    def sign_in(self) -> SignInOutputDto:
        uid = self._input_dto.uid
        simple_pw = eventLoop.run_until_complete(UserRepo(uid).find_simple_pw())
        token = SignInDomainService(uid).get_token(self._input_dto.simple_pw, simple_pw)
        return SignInOutputDto(token)
