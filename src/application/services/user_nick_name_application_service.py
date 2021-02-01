from dataclasses import asdict

from src.application.dto.users_dto import NickNameDto, NickNameInputDto, NickNameOutputDto
from src.application.repository.user_repository import UserRepo


class NickNameApplicationService:
    def __init__(self, input_dto: NickNameInputDto):
        self._inpnut_dto = input_dto

    def update_nick_name(self) -> NickNameOutputDto:
        uid              = self._inpnut_dto.uid
        new_nick_name    = self._inpnut_dto.nick_name
        user_repo        = UserRepo(uid)
        nick_name_params = NickNameDto(new_nick_name)

        user_repo.update_user_info(asdict(nick_name_params))
        return NickNameOutputDto(new_nick_name)

