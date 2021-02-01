from decimal import Decimal
from datetime import datetime as dt
from dataclasses import asdict

from src.domain.value.filed import datetimeFiled, priceFiled, rateOfReturnFiled, qtyFiled, assetFiled, pricePercentChangeFiled, baseQtyFiled
from src.application.dto.users_dto import UserChartOutputDto
from src.domain.value.data import defualtOutputDatetime

class UserChartDomainService:

    @staticmethod
    def get_base_qty(count, current_list, tot_base_qty):
        if count == 0:
            base_qty = Decimal(current_list[count]['buy_qty'])
            return base_qty
        elif current_list[count]['buy_datetime'] == current_list[count - 1]['buy_datetime']:
            base_qty = Decimal(current_list[count]['buy_qty'])
            return 0
        else:
            base_qty = Decimal(current_list[count]['buy_qty']) + Decimal(current_list[count - 1]['buy_qty'])
            return base_qty

    @staticmethod
    def get_chart_data(current_list):
        chart_list = []
        tot_base_qty = 0
        for i in range(len(current_list)):
            col_base_qty = UserChartDomainService.get_base_qty(i, current_list, tot_base_qty)
            tot_base_qty += col_base_qty
            print(tot_base_qty)

            datetime = dt.strftime(current_list[i][datetimeFiled], defualtOutputDatetime)
            price = float(current_list[i][priceFiled])
            # rate_of_return = float(current_list[i][rateOfReturnFiled])
            qty = float(tot_base_qty)
            asset = float(Decimal(tot_base_qty) * Decimal(current_list[i][priceFiled]))
            price_percent_change = float(current_list[i][pricePercentChangeFiled])

            chart_data = UserChartOutputDto(datetime, price, qty, asset, price_percent_change)
            chart_list.append(asdict(chart_data))
        return chart_list

    @staticmethod
    def get_newly_price_list(newst_buy_list, newst_fund_issue_list):
        newst_price_list = []
        for newst_fund in newst_fund_issue_list:
            newst_fund_issue = list(filter(lambda newset_buy_list: newset_buy_list[datetimeFiled] <= newst_fund[datetimeFiled], newst_buy_list))
            newst_fund['buy_qty'] = newst_fund_issue[0][baseQtyFiled]
            newst_fund['buy_datetime'] = newst_fund_issue[0][datetimeFiled]
            newst_price_list.append(newst_fund)
        return newst_price_list