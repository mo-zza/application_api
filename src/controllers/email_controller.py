from flask import request

from src.controllers import email_bp as bp
from src.application.dto.email_dto import EmailInputDto, CheckOTPInputDto
from src.application.services.email_application_service import EmailApplicationService
from src.adapter.user_athentication import EmailAuth
from src.adapter.response import success_response
from src.domain.value.data import eventLoop
from src.domain.value.controller_data import userEmailArg, otpArg


@bp.route('', methods=['POST'])
@EmailAuth
def send_otp(uid):
    user_email = request.form[userEmailArg]
    input_dto  = EmailInputDto(user_email, uid)
    email_send = EmailApplicationService(input_dto).send_mail()
    return success_response(email_send, 200)

@bp.route('', methods=['GET'])
@EmailAuth
def otp_check(uid):
    user_email       = request.args.get(otpArg)
    req_otp          = request.args.get('otp')
    input_dto        = CheckOTPInputDto(uid, user_email, req_otp)
    result_otp_check = EmailApplicationService(input_dto).check_otp()
    return success_response(result_otp_check, 200)
