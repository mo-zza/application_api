from src.application.repository.user_repository import UserRepo
from src.application.dto.users_dto import SignUpInputDto, SignUpOutputDto
from src.domain.services.sign_up_domain_service import SignUpDomainService
from src.domain.value.filed import createTimeFiled, depositAddressFiled, userEmailFiled, userStatusFiled
from src.domain.value.data import eventLoop

class SignUpApplicationService:
    def __init__(self, input_dto: SignUpInputDto):
        self._input_dto = input_dto

    async def get_available_acount(self, sign_up_domain_service, uid, available_account_list):
        # sign_up_domain_service.check_account_count(available_account_list=available_account_list, uid=uid)
        available_account = sign_up_domain_service.available_account(available_account_list=available_account_list, uid=uid)
        return available_account

    def create_user(self) -> SignUpOutputDto:
        uid                    = self._input_dto.uid
        email_noti             = self._input_dto.email_notice
        push_noti              = self._input_dto.push_notice
        noti_token             = self._input_dto.notice_token
        user_repo              = UserRepo(uid)
        nick_name              = user_repo.find_user_display_name(self._input_dto.user_email)
        profile_url            = user_repo.find_user_profile_url(self._input_dto.user_email)
        sign_up_domain_service = SignUpDomainService(UserRepo)
        available_account_list = user_repo.find_available_sub_account_list()

        available_account = eventLoop.run_until_complete(self.get_available_acount(sign_up_domain_service=sign_up_domain_service,
                                                                                    uid=uid,
                                                                                    available_account_list=available_account_list))

        user_private, user_public, notice_params = sign_up_domain_service.allocated_to_user(uid=uid,
                                                                                            available_account=available_account,
                                                                                            user_email=self._input_dto.user_email,
                                                                                            simple_pw=self._input_dto.simple_pw,
                                                                                            nick_name=nick_name,
                                                                                            profile_url=profile_url,
                                                                                            email_notice=email_noti,
                                                                                            push_notice=push_noti,
                                                                                            notice_token=noti_token)

        user_repo.save_user_initial_set(available_account=available_account,
                                        uid=uid,
                                        private_user_params=user_private,
                                        public_user_params=user_public,
                                        notice_params=notice_params)

        created_datetime  = user_public[createTimeFiled]
        deposit_addresses = user_public[depositAddressFiled]
        user_email        = user_public[userEmailFiled]
        status            = user_public[userStatusFiled]
        return SignUpOutputDto(created_datetime=created_datetime, deposit_addresses=deposit_addresses, email=user_email, status=status, uid=uid)