from flask import request

from src.controllers import withdrawal_bp as bp
from src.application.dto.withdrawal_dto import WithdrawalInputDto, CancelWithdrawalInputDto
from src.application.services.withdrawal_application_service import WithdrawalApplicationService
from src.adapter.response import success_response
from src.adapter.user_athentication import EmailAuth
from src.infrastructure.multi_thread import ThreadProcess
from src.domain.value.controller_data import defaultReqFund
from src.domain.value.controller_data import userEmailArg, fundNameArg

    
@bp.route('', methods=['GET'])
@EmailAuth
def get_withdrawal_info(uid):
    user_email      = request.args.get(userEmailArg)
    fund_name       = request.args.get(fundNameArg, defaultReqFund)
    input_dto       = WithdrawalInputDto(uid, user_email, fund_name)
    withdrawal_info = WithdrawalApplicationService(input_dto).create_withdrawal_receipt()
    return success_response(withdrawal_info, 200)

@bp.route('status', methods=['DELETE'])
@EmailAuth
def cancel_withdrawal(uid):
    request.args.get(userEmailArg)
    input_dto     = CancelWithdrawalInputDto(uid)
    cancel_result = WithdrawalApplicationService(input_dto).cancel_withdrawal()
    return success_response(cancel_result, 200)