from datetime import datetime as dt
from decimal import Decimal
from dataclasses import asdict

from src import binance
from src.application.dto.withdrawal_dto import WithdrawalCancelDto
from src.domain.value.filed import assetFiled, usdtFiled, newStatusFiled, canceldFiled
from src.domain.value.data import currentDatetime, navCalculationRotation, koreaDatetime
from src.infrastructure.multi_thread import ThreadProcess
from src.domain.value.exceptions import ZeroRecord

class WithdrawalDomainService:
    def __init__(self, uid):
        self.uid = uid
        self.binance = binance

    async def get_newest(self, order_list):
        if len(order_list) <= 0:
            raise ZeroRecord('withdrawal')
        else:
            order_newest = order_list[0].to_dict()
        return order_newest

    def calculate_remaining_seconds(self):
        utcnow = currentDatetime
        start_datetime = dt(utcnow.year, utcnow.month, utcnow.day, hour=7)
        remaining_seconds = (start_datetime - utcnow).total_seconds()
        while True:
            if remaining_seconds > 0:
                break
            else:
                remaining_seconds += navCalculationRotation
        return int(remaining_seconds)

    async def get_remaining_secound(self, status):
        if status == 'new':
            remaining_seconds = ThreadProcess(target=self.calculate_remaining_seconds(), args=None)
        else:
            remaining_seconds = 0
        return remaining_seconds

    def get_usdt_exchange_rate(self, assetFiled):
        if assetFiled == usdtFiled:
            return Decimal('1')
        else:
            symbol = assetFiled + usdtFiled
            return self.binance.get_mid_price(symbol)
            
    def calculate_withdrawal_amt_range(self, asset_value, exchange_rate):
        expected_amt_high = round(Decimal('1.05') * asset_value / exchange_rate, 8)
        expected_amt_low  = round(Decimal('0.95') * asset_value / exchange_rate, 8)
        return expected_amt_high, expected_amt_low

    def record_cancle_withdrawal(self, status):
        if status != newStatusFiled:
            raise ZeroRecord('new withdrawal')
        status_params = WithdrawalCancelDto(canceldFiled, koreaDatetime)
        return status_params
