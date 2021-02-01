from flask import request

from src.controllers import fund_bp as bp
from src.application.dto.fund_dto import FundInputDto
from src.application.services.fund_application_service import FundApplicationService
from src.domain.value.data import defaultStart, defaultLimit, defaultInterval
from src.adapter.response import success_response
from src.adapter.user_athentication import EmailAuth
from src.domain.value.controller_data import fundNameArg, defaultReqFund, startArg, limitArg, intervalArg, userEmailArg


@bp.route('MoneyFlowHistory', methods=['GET'])
def get_fund_money_flow_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    interval  = defaultInterval

    input_dto = FundInputDto(fund_name=fund_name, interval=interval)
    money_flow_history = FundApplicationService(input_dto).money_flow_history()
    return success_response(money_flow_history, 200)

@bp.route('priceHistory', methods=['GET'])
def get_fund_price():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto  = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    fund_price = FundApplicationService(input_dto).fund_price()
    return success_response(fund_price, 200)

@bp.route('RateofReturnHistory', methods=['GET'])
def get_rateo_return_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    rateo_reutrn_history = FundApplicationService(input_dto).fund_rate_of_returns()
    return success_response(rateo_reutrn_history, 200)

@bp.route('cumReturn', methods=['GET'])
def get_cum_return():
    fund_name  = request.args.get(fundNameArg, defaultReqFund)
    input_dto  = FundInputDto(fund_name=fund_name)
    cum_return = FundApplicationService(input_dto).cummulative_return()
    return success_response(cum_return, 200)

@bp.route('returnHistory', methods=['GET'])
def get_reuturn_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    resturn_history = FundApplicationService(input_dto).fund_returns()
    return success_response(resturn_history, 200)

@bp.route('fundingHistory', methods=['GET'])
def get_funding_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    funding_history = FundApplicationService(input_dto).get_fund_fundings()
    return success_response(funding_history, 200)

@bp.route('depositHistory', methods=['GET'])
def get_deposit_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    deposit_history = FundApplicationService(input_dto).deposits()
    return success_response(deposit_history, 200)

@bp.route('withdrawalHistory', methods=['GET'])
def get_withdrawal_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    withdrawal_history = FundApplicationService(input_dto).withdrawals()
    return success_response(withdrawal_history, 200)

@bp.route('pricePercentHistory', methods=['GET'])
def get_price_percent_history():
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    start     = request.args.get(startArg, defaultStart)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, start=start, limit=limit, interval=interval)
    price_pervent_history = FundApplicationService(input_dto).fund_price_percent()
    return success_response(price_pervent_history, 200)

@bp.route('balanceHistory', methods=['GET'])
@EmailAuth
def get_balance_history(uid):
    request.args.get(userEmailArg)
    fund_name = request.args.get(fundNameArg, defaultReqFund)
    limit     = int(request.args.get(limitArg, defaultLimit))
    interval  = request.args.get(intervalArg, defaultInterval)

    input_dto = FundInputDto(fund_name=fund_name, limit=limit, interval=interval, uid=uid)
    balance_history = FundApplicationService(input_dto).balance_history()
    return success_response(balance_history, 200)

@bp.route('portChart', methods=['GET'])
def get_fund_port_chart():
    fund_name  = request.args.get(fundNameArg, defaultReqFund)
    input_dto  = FundInputDto(fund_name)

    port_chart = FundApplicationService(input_dto).fund_port_chart()
    return success_response(port_chart, 200)

@bp.route('asset', methods=['GET'])
def get_fund_asset():
    fund_name  = request.args.get(fundNameArg, defaultReqFund)
    input_dto  = FundInputDto(fund_name)

    asset_chart = FundApplicationService(input_dto).fund_asset()
    return success_response(asset_chart, 200)

@bp.route('report', methods=['GET'])
def get_fund_report():
    fund_name  = request.args.get(fundNameArg, defaultReqFund)
    input_dto  = FundInputDto(fund_name)

    report_chart = FundApplicationService(input_dto).fund_report()
    return success_response(report_chart, 200)