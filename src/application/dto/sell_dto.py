from dataclasses import dataclass
import datetime

from src.domain.value.filed import newStatusFiled


@dataclass
class SellInputDto:
    uid: str
    user_email: str
    asset: str
    network: str
    address: str
    fund_name: str

@dataclass
class SellOutputDto:
    message: str

@dataclass
class OrderInputDto:
    uid: str
    order_id: str
    datetime: int
    fund_name: str
    user_qty: str

@dataclass
class WithdrawalInputDto:
    order_id: str
    datetime: int
    asset: str
    network: str
    address: str

@dataclass
class WithdrawDto:
    uid: str
    order_id: str
    address: str
    asset: str
    network: str
    network_commission: str
    datetime: datetime
    updated_datetime : datetime
    status: str = 'new'
    asset_value: str = ""
    asset_qty: str = ""
    exchange_id: str = ""
    withdraw_id: str = ""
    transfer_type: str = ""
    tx_id: str = ""
    balance: str = ""

@dataclass
class OrderDto:
    uid: str
    order_id: str
    fund_name: str
    side: str
    base_qty: str
    datetime: datetime
    updated_datetime: datetime
    status: str = newStatusFiled
    price: str = ""
    quote_qty: str = ""
    status: str = newStatusFiled