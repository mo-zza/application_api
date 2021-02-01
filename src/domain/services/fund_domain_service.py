import pandas as pd
from dataclasses import asdict
from datetime import datetime as dt

from src.application.dto.fund_dto import FundDomainInputDto, FundPortChartDto, FundAssetDto, FundReportDto
from src.domain.value.filed import datetimeFiled, qtyFiled, priceFiled, totalQtyFiled, pricePercentChangeFiled, ReturnFiled, rateOfReturnFiled, mddFiled\
    , sharpeRatioFiled, totalPrincipalFiled, totalProfitFiled, volatilityFiled, totalAssetFiled
from src.domain.value.exceptions import ZeroFundAsset, ZeroFunding, ZeroBalance, InsuffiientError
from src.domain.value.data import defualtOutputDatetime

class FundDomainService:
    def __init__(self, input_dto: FundDomainInputDto):
        self.input_dto = input_dto

    def build_asset_history(self, rounding=4):
        asset_history = dict()
        for snapshot in self.input_dto.snapshot:
            issue = snapshot.to_dict()
            try:
                issue_datetime = issue[datetimeFiled]
                element = float(issue[self.input_dto.condition[0]])
            except KeyError:
                raise ZeroFundAsset(snapshot.id)
            else:
                asset_history[issue_datetime] = element
        return asset_history

    def build_trascation_history(self, roundfing=4):
        transcation_history = dict()
        for snapshot in self.input_dto.snapshot:
            issue = snapshot.to_dict()
            try:
                issue_datetime = issue[datetimeFiled]
                element = float(issue[self.input_dto.condition[0]]) * float(issue[self.input_dto.condition[1]])
            except KeyError:
                raise ZeroFunding(snapshot.id)
            else:
                transcation_history[issue_datetime] = element
        return transcation_history

    def build_cum_return(self, rounding):
        initial_price = float(self.input_dto.snapshot[0].to_dict()[self.input_dto.condition[0]])
        final_price   = float(self.input_dto.snapshot[-1].to_dict()[self.input_dto.condition[0]])
        cum_return    = round(final_price/initial_price, rounding)
        return cum_return

    def check_user_balance(self, user_fund_history):
        balance = user_fund_history[0].to_dict()
        qty     = float(balance[qtyFiled])

        if user_fund_history == [] or qty <= 0:
            raise ZeroBalance()
        start = balance[datetimeFiled].strftime(defualtOutputDatetime)
        return qty, start

    def build_trading_dataframe(self, deposit_history, withdrawal_history, funding_history, interval):
        try:
            deposits    = pd.Series(deposit_history, name='funddeposit').resample(interval).sum()
            withdrawals = pd.Series(withdrawal_history, name='fundwithdraw').resample(interval).sum()
            fundings    = pd.Series(funding_history, name='fundingprofit').resample(interval).sum()

            dataframe = deposits.to_frame().join(withdrawals).join(fundings)
            dataframe[datetimeFiled] = dataframe.index.strftime('%Y-%m-%d')
            dataframe = dataframe.dropna(axis=0)
            return dataframe
        except:
            raise InsuffiientError

    def build_fund_port_chart(self):
        port_data_list = []
        cum_rate_of_return = 1
        for rate_of_return in self.input_dto.snapshot:
            rate_of_return_price   = float(rate_of_return.to_dict()[rateOfReturnFiled])
            cum_rate_of_return     = rate_of_return_price * cum_rate_of_return
            rate_of_return_percent = (cum_rate_of_return - 1) * 100
            
            datetime      = rate_of_return.to_dict()[datetimeFiled]
            day_percent   = float(rate_of_return.to_dict()[pricePercentChangeFiled])
            total_percent = float(rate_of_return_percent)
            day_return    = float(rate_of_return.to_dict()[ReturnFiled])
            total_qty     = float(rate_of_return.to_dict()[totalQtyFiled])
            datestr       = dt.strftime(rate_of_return.to_dict()[datetimeFiled], "%Y-%m-%d")
            timestr       = dt.strftime(rate_of_return.to_dict()[datetimeFiled], "%H:%M:%S")
            
            port_data = FundPortChartDto(datetime=datetime,
                                        day_percent=day_percent,
                                        total_percent=total_percent,
                                        day_return=day_return,
                                        total_qty=total_qty,
                                        datestr=datestr,
                                        timestr=timestr)
                                        
            port_data_list.append(asdict(port_data))
        return port_data_list

    def build_asset_chart(self):
        asset_list = []
        for asset in self.input_dto.snapshot:
            fund_asset = float(asset.to_dict()[totalQtyFiled]) * float(asset.to_dict()[priceFiled])

            asset_data = FundAssetDto(fund_asset)
            asset_list.append(asdict(asset_data))
        return asset_list

    def build_report_chart(self):
        report_chart_list = []
        for report_chart in self.input_dto.snapshot:
            datetime = report_chart.to_dict()[datetimeFiled]
            mdd = float(report_chart.to_dict()[mddFiled])
            rate_of_return = float(report_chart.to_dict()[rateOfReturnFiled])
            sharpe_ratio = float(report_chart.to_dict()[sharpeRatioFiled])
            total_asset = float(report_chart.to_dict()[totalAssetFiled])
            total_principal = float(report_chart.to_dict()[totalPrincipalFiled])
            total_profit = float(report_chart.to_dict()[totalPrincipalFiled])
            volatility = float(report_chart.to_dict()[volatilityFiled])
            datestr = dt.strftime(report_chart.to_dict()[datetimeFiled], "%Y-%m-%d")
            timestr = dt.strftime(report_chart.to_dict()[datetimeFiled], "%H:%M:%S")

            report_data = FundReportDto(datetime, mdd, rate_of_return, sharpe_ratio, total_asset, total_principal, total_profit, volatility, datestr, timestr)
            report_chart_list.append(asdict(report_data))
        return report_chart_list
