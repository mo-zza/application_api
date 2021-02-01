from dataclasses import dataclass
from datetime import datetime


@dataclass
class WithdrawalInputDto:
    uid: str
    user_email: str
    fund_name: str = 'ZLBUSDT'

@dataclass
class WithdrawalOutputDto:
    uid: str
    status: str
    asset: str
    network: str
    withdrawal_address: str
    remaining_secounds: str
    expected_amt_high: str
    expected_amt_low: str
    investment_principal: str
    inbestment_profit: str
    withdrawal_fee: str

@dataclass
class WithdrawalCancelDto:
    status: str
    updated_datetime: datetime

@dataclass
class CancelWithdrawalInputDto:
    uid: str