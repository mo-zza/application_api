from dataclasses import dataclass
from datetime import datetime as dt
import datetime

from src.domain.entities.users_entity import UserEmail, SimplePw
from src.domain.value.filed import newStatusFiled, datetimeFiled
from src.domain.value.data import defualtOutputDatetime
from src.domain.value.exceptions import VerifyPassword


@dataclass
class SignInInputDto:
    def __init__(self, uid, simple_pw):
        self.uid = uid
        self.simple_pw = simple_pw

@dataclass(frozen=True)
class SignInOutputDto:
    access_token: str

@dataclass
class PasswordInputDto:
    def __init__(self, uid, user_email, simple_pw=None):
        if simple_pw:
            self.simple_pw = simple_pw
        self.user_email = user_email
        self.uid = uid

@dataclass(frozen=True)
class PasswordOutPutDto:
    simple_pwd : str

@dataclass
class SignUpInputDto:
    uid: str
    user_email : str
    simple_pw: str
    email_notice: bool
    push_notice: bool
    notice_token: str = None

@dataclass
class SignUpOutputDto:
    created_datetime : datetime
    deposit_addresses : dict
    email : str
    status : str
    uid : str
    withdrawal_addresses : str = ""

@dataclass
class AllocateAccountToUser:
    deposit_addresses: str
    sub_account_id: str

@dataclass
class SimpleInputDto:
    user_email: str
    uid: str

@dataclass
class SimpleOutPutDto:
    data_list: list

@dataclass
class AssetOutputDto:
    total_base_qty: float
    total_return: float
    yield_return: float
    total_asset: float
    btc_withdrawal_fee: float
    usdt_withdrawal_fee: float

@dataclass
class UserChartOutputDto:
    datetime : datetime
    price : float
    # rate_of_return : float
    qty : float
    asset : float
    price_pct_change : float

@dataclass
class PublicUserDto:
    created_datetime: datetime
    uid: str
    email: str
    deposit_addresses: dict
    nick_name: str
    profile_url: str
    withdrawal_addresses: str = ""
    status: str = newStatusFiled

@dataclass
class PrivateUserDto:
    uid: str
    email: str
    simple_pwd: str
    status: str = newStatusFiled

@dataclass
class NoticeDto:
    user_email: str
    email_notice_on: str
    push_notice_on: str
    notice_token: str

@dataclass
class SubAccountDto:
    sub_account_id: str
    sub_account_email: str
    api_key: str
    secret_key: str
    deposit_addresses: dict
    occupied: bool = False

@dataclass
class PasswordDto:
    simple_pwd: str

@dataclass
class HistoryDto:
    type: str
    asset: list
    qty: list
    datetime: list
    datastr: list
    timestr: list

@dataclass
class NickNameInputDto:
    uid: str
    nick_name: str

@dataclass
class NickNameDto:
    nick_name: str

@dataclass
class NickNameOutputDto:
    nick_name: str

@dataclass
class ProfileInputDto:
    uid: str
    profile: str

@dataclass 
class ProfileDto:
    profile_url: str

@dataclass
class ProfileOutputDto:
    profile_url: str

def user_hisotry_output(trans_type, asset_snapshot, asset, qty):
    asset_doc = {
        "type": trans_type,
        "asset" : asset_snapshot.to_dict()[asset],
        "datetime" : asset_snapshot.to_dict()[datetimeFiled],
        "datestr": dt.strftime(asset_snapshot.to_dict()[datetimeFiled], "%Y-%m-%d"),
        "timestr": dt.strftime(asset_snapshot.to_dict()[datetimeFiled], "%H:%M:%S")
        }
    return asset_doc