from flask import request

from src.controllers import sell_bp as bp
from src.application.dto.sell_dto import SellInputDto
from src.application.services.apply_sell_application_service import ApplySellApplicationService
from src.adapter.response import success_response
from src.adapter.user_athentication import EmailAuth
from src.domain.value.controller_data import userEmailArg, assetArg, networkArg, addressArg, fundNameArg


@bp.route('', methods=['POST'])
@EmailAuth
def order_sell(uid):
    user_email = request.form[userEmailArg]
    asset      = request.form[assetArg]
    network    = request.form[networkArg]
    address    = request.form[addressArg]
    fund_name  = request.form[fundNameArg]

    input_dto = SellInputDto(uid, user_email, asset, network, address, fund_name)
    order_result = ApplySellApplicationService(input_dto).create_order()
    return success_response(order_result, 200)