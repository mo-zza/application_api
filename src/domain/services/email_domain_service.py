from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import render_template
from flask_mail import Message
import random
from dataclasses import asdict

from src.application.dto.email_dto import CheckEmailInputDto, EmailCountDto, UserLock
from src.domain.entities.email_entity import ArgonEntity
from src.domain.value.otp import emailTemplate, emailTitle, emailBody, emailSender
from src.domain.value.collection import usersCol, otpCol
from src.domain.value.filed import lockStatusFiled
from src.domain.value.exceptions import LockedUser, VerifyOTP


class EmailDomainService:
    def __init__(self, argon_entity: ArgonEntity):
        self._argon_entity = argon_entity

    def create_crypt_num(self, argon_entity: ArgonEntity):
        memory_cost = argon_entity.memoryCostLow << argon_entity.memoryCostHigh
        otp = random.randint(argon_entity.randomLow, argon_entity.randomHigh)
        hasher = PasswordHasher(argon_entity.timeCost, memory_cost, argon_entity.parallelism)
        str_otp = str(otp)
        crypt_otp = hasher.hash(str_otp)
        return otp, crypt_otp, hasher

    async def create_template(self, user_email):
        otp, hash_otp, _ = self.create_crypt_num(self._argon_entity)
        html_template    = render_template(emailTemplate, OTP=otp)

        email_msg      = Message(emailTitle, sender=emailSender, recipients=[user_email])
        email_msg.body = emailBody
        email_msg.html = html_template
        return otp, hash_otp, email_msg

    def check_user_status(self, email_repo, false_count, uid):
        count_params  = EmailCountDto(false_count + 1)
        status_params = UserLock(lockStatusFiled)

        if false_count >= 5:
            email_repo.update_user_status(asdict(status_params))
            raise LockedUser
        email_repo.update_false_count(asdict(count_params))
        raise VerifyOTP

    def check_otp(self, email_input: CheckEmailInputDto):
        user_status  = email_input.user_status
        crypto_otp   = email_input.crypto_otp
        req_otp      = email_input.req_otp
        false_count  = email_input.false_count
        uid          = email_input.uid
        email_repo   = email_input.repo
        _, _, hasher = self.create_crypt_num(self._argon_entity)
        
        if user_status == lockStatusFiled:
            raise LockedUser
        try:
            hasher.verify(crypto_otp, req_otp)
            return 'correct'
        except:
            self.check_user_status(email_repo, false_count, uid)