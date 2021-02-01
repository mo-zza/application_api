from src.application.dto.users_dto import ProfileInputDto, ProfileOutputDto, ProfileDto
from src.application.repository.user_repository import UserRepo


class ProfileUploadApplication:
    def __init__(self, input_dto: ProfileInputDto):
        self._input_dto = input_dto

    def upload_profile(self) -> ProfileOutputDto:
        uid       = self._input_dto.uid
        profile   = self._input_dto.profile
        user_repo = UserRepo(uid)

        profile_dto = ProfileDto(profile)
        user_repo.save_user_profile(profile_dto)
        return ProfileOutputDto(profile)