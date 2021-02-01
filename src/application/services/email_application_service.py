from flask_mail import Message
from dataclasses import asdict

from src import mail_server as mail
from src.application.repository.email_repository import EmailRepo
from src.application.dto.email_dto import EmailInputDto, EmailOutputDto, EmailDto, CheckOTPInputDto, CheckOTPOutputDto, CheckEmailInputDto
from src.domain.services.email_domain_service import EmailDomainService
from src.domain.entities.email_entity import ArgonEntity
from src.domain.value.otp import emailBody, emailSender, emailTitle
from src.domain.value.data import eventLoop


class EmailApplicationService:

    def __init__(self, input_dto: EmailInputDto or CheckOTPInputDto):
        self._input_dto = input_dto

    def send_mail(self) -> EmailOutputDto:
        otp, hash_otp, email_msg = eventLoop.run_until_complete(\
            EmailDomainService(ArgonEntity('private')).create_template(self._input_dto.user_email))
        otp_params = EmailDto(hash_otp)

        EmailRepo(self._input_dto.uid).save_otp(asdict(otp_params))
        mail().send(email_msg)

        return EmailOutputDto(otp, hash_otp)

    async def get_user_otp_info(self, email_repo):
        crypto_otp, false_count = email_repo.find_otp_info()
        user_status             = email_repo.find_user_status()
        return crypto_otp, false_count, user_status


    def check_otp(self) -> CheckOTPOutputDto:
        req_otp       = self._input_dto.req_otp
        uid           = self._input_dto.uid
        email_repo    = EmailRepo(uid)
        argon_entity  = ArgonEntity('private')

        crypto_otp, false_count, user_status = eventLoop.run_until_complete(self.get_user_otp_info(email_repo))

        email_input = CheckEmailInputDto(req_otp, crypto_otp, user_status, false_count, uid, email_repo)
        checked_otp = EmailDomainService(argon_entity).check_otp(email_input)
        return CheckOTPOutputDto(checked_otp)