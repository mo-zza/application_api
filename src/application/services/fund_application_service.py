import pandas as pd
from dataclasses import asdict

from src.application.repository.fund_repository import FundRepo
from src.application.dto.fund_dto import FundInputDto, FundDomainInputDto, create_series, FundOutputDto
from src.domain.services.fund_domain_service import FundDomainService
from src.domain.value.filed import priceFiled, profitFiled, ReturnFiled, cumIssueQtyFiled, cumBurnQtyFiled, pricePercentChangeFiled
from src.domain.value.data import rounding, defualtOutputDatetime
from src.domain.value.exceptions import InsuffiientError


class FundApplicationService:
    def __init__(self, input_dto: FundInputDto):
        self._input_dto = input_dto
        self._fund_repo = FundRepo()

    def fund_price(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [priceFiled])
        price_history          = FundDomainService(domain_input).build_asset_history(rounding)
        
        if len(price_history) <= 0:
            raise InsuffiientError
        prices = pd.Series(price_history).resample(interval).bfill()
        series = create_series(prices, start, limit, rounding)
        return FundOutputDto(series.to_dict())

    def fund_rate_of_returns(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [priceFiled])
        price_history          = FundDomainService(domain_input).build_asset_history(8)

        if len(price_history) <= 1:
            raise InsuffiientError
        prices = pd.Series(price_history).resample(interval).bfill()
        daily_returns = 1 + prices.pct_change().dropna()
        series = create_series(daily_returns, start, limit, 8)
        return FundOutputDto(series.to_dict())

    def cummulative_return(self):
        fund_name              = self._input_dto.fund_name
        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [priceFiled])

        if len(issue_history_snapshot) <= 0:
            raise InsuffiientError
        cum_return = FundDomainService(domain_input).build_cum_return(rounding)
        return FundOutputDto(cum_return)

    def fund_returns(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [ReturnFiled])
        return_history         = FundDomainService(domain_input).build_asset_history(rounding)

        if len(return_history) <= 0:
            raise InsuffiientError
        profits = pd.Series(return_history).resample(interval).sum()
        series  = create_series(profits, start, limit, rounding)
        return FundOutputDto(series.to_dict())

    def get_fund_fundings(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        funding_history        = self._fund_repo.find_funding_history(fund_name)      
        domain_input           = FundDomainInputDto(funding_history, [profitFiled])
        profit_history         = FundDomainService(domain_input).build_asset_history(rounding)  

        if len(profit_history) <= 0:
            raise InsuffiientError
        funding = pd.Series(profit_history).resample(interval).sum()
        series  = create_series(funding, start, limit, rounding)
        return FundOutputDto(series.to_dict()) 

    def deposits(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [cumIssueQtyFiled, priceFiled])
        deposit_history        = FundDomainService(domain_input).build_trascation_history(rounding)

        if len(deposit_history) <= 0:
            raise InsuffiientError
        deposits = pd.Series(deposit_history).resample(interval).sum()
        series  = create_series(deposits, start, limit, rounding)
        return FundOutputDto(series.to_dict())

    def withdrawals(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [cumBurnQtyFiled, priceFiled])
        withdrawal_history     = FundDomainService(domain_input).build_trascation_history(rounding)

        if len(withdrawal_history) <= 0:
            raise InsuffiientError
        withdrawals = pd.Series(withdrawal_history).resample(interval).sum()
        series  = create_series(withdrawals, start, limit, rounding)
        return FundOutputDto(series.to_dict())
    
    def fund_price_percent(self):
        fund_name = self._input_dto.fund_name
        start     = pd.to_datetime(self._input_dto.start).strftime(defualtOutputDatetime)
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        issue_history_snapshot = self._fund_repo.find_fund_issue_history(fund_name)
        domain_input           = FundDomainInputDto(issue_history_snapshot, [pricePercentChangeFiled])
        price_percent_history  = FundDomainService(domain_input).build_asset_history(rounding)

        if len(price_percent_history) <= 0:
            raise InsuffiientError
        funding = pd.Series(price_percent_history).resample(interval).sum()
        series  = create_series(funding, start, limit, rounding)
        return FundOutputDto(series.to_dict()) 

    def balance_history(self):
        uid       = self._input_dto.uid
        fund_name = self._input_dto.fund_name
        limit     = self._input_dto.limit
        interval  = self._input_dto.interval

        user_fund_history = self._fund_repo.find_user_fund_history(uid, fund_name)
        funding_history   = self._fund_repo.find_fund_issue_history(fund_name)
        user_domain_input = FundDomainInputDto(funding_history, [priceFiled])
        qty, start        = FundDomainService(user_domain_input).check_user_balance(user_fund_history)
        price_history     = FundDomainService(user_domain_input).build_asset_history(rounding)

        if len(price_history) <= 0:
            raise InsuffiientError
        prices = pd.Series(price_history).resample(interval).sum()
        user_balance = qty * prices
        series = create_series(user_balance, start, limit, rounding)
        return FundOutputDto(series.to_dict())

    def money_flow_history(self):
        fund_name = self._input_dto.fund_name
        interval  = self._input_dto.interval
        fund_repo = FundRepo()

        issue_snapshot   = fund_repo.find_fund_issue_history(fund_name)
        funding_snapshot = fund_repo.find_funding_history(fund_name)

        deposit_domain_input    = FundDomainInputDto(issue_snapshot, [cumIssueQtyFiled, priceFiled])
        withdrawal_domain_input = FundDomainInputDto(issue_snapshot, [cumBurnQtyFiled, priceFiled])
        funding_domain_input    = FundDomainInputDto(funding_snapshot, [profitFiled])

        deposit_history    = FundDomainService(deposit_domain_input).build_trascation_history()
        withdrawal_history = FundDomainService(withdrawal_domain_input).build_trascation_history()
        funding_history    = FundDomainService(funding_domain_input).build_asset_history()

        dataframe = FundDomainService(deposit_domain_input).build_trading_dataframe(deposit_history, withdrawal_history, funding_history, interval)
        return FundOutputDto(dataframe.to_dict(orient='records'))

    def fund_port_chart(self):
        fund_name         = self._input_dto.fund_name
        issue_snapshot    = FundRepo().find_fund_issue_list_order_datetime(fund_name)
        fund_domain_ipnut = FundDomainInputDto(issue_snapshot) 

        port_chart_list = FundDomainService(fund_domain_ipnut).build_fund_port_chart()
        return FundOutputDto(port_chart_list)

    def fund_asset(self):
        fund_name         = self._input_dto.fund_name
        issue_snapshot    = FundRepo().find_fund_issue_list_order_datetime(fund_name)
        fund_domain_input = FundDomainInputDto(issue_snapshot)

        asset_chart = FundDomainService(fund_domain_input).build_asset_chart()
        last_asset  = asset_chart[-1]
        return last_asset

    def fund_report(self):
        fund_name         = self._input_dto.fund_name
        report_snapshot   = FundRepo().find_report_list_order_datetime(fund_name)
        fund_domain_input = FundDomainInputDto(report_snapshot)
        
        report_chart = FundDomainService(fund_domain_input).build_report_chart()
        return FundOutputDto(report_chart[-1])
        