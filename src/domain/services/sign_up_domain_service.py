import threading
from dataclasses import asdict

from src import binance, firestore
from src.domain.value.data import currentDatetime, numberOfAccountCreation, mininumNumberOfAccounts
from src.application.repository.user_repository import UserRepo
from src.application.dto.users_dto import PrivateUserDto, PublicUserDto, SubAccountDto, NoticeDto
from src.domain.value.filed import depositAddressFiled, subAccountIDFiled, usdtFiled, btcFiled, usdtNetworkFiled, btcNetworkFiled, addressFiled,\
    subAccountApiKeyFiled, subAccountSecretKeyFiled, btcFiled, btcNetworkFiled, usdtFiled, usdtNetworkFiled
from src.domain.value.data import subAccountIdBinance, apikeyBinance, secretBinance
from src.infrastructure.multi_thread import ThreadProcess
from src.domain.value.exceptions import NonAvailableAccount, BinanceError

class SignUpDomainService:
    def __init__(self, user_repo: UserRepo):
        self.binance    = binance
        self.firestore  = firestore
        self._user_repo = user_repo

    def create_sub_account(self, uid):
        sub_id            = self.binance.create_sub_account()[subAccountIdBinance]
        sub_email         = self.binance.get_sub_account_email(sub_id)
        usdt_addr         = self.binance.get_sub_account_deposit_address(email=sub_email, coin=usdtFiled, network=usdtNetworkFiled)[addressFiled]
        btc_addr          = self.binance.get_sub_account_deposit_address(email=sub_email, coin=btcFiled, network=btcNetworkFiled)[addressFiled]
        api_info          = self.binance.create_sub_account_api_key(sub_account_id=int(sub_id))
        try:
            api_key           = api_info[apikeyBinance]
            secret_key        = api_info[secretBinance]
            deposit_addresses = {btcFiled : {btcNetworkFiled : btc_addr}, usdtFiled : {usdtNetworkFiled : usdt_addr}}

            account_params = asdict(SubAccountDto(sub_account_id=sub_id,
                                                sub_account_email=sub_email,
                                                api_key=api_key,
                                                secret_key=secret_key,
                                                deposit_addresses=deposit_addresses))
                                                
            self._user_repo(uid).save_account(sub_id, account_params)
            return account_params
        except:
            raise BinanceError


    def check_account_count(self, available_account_list, uid):
        target = self.create_sub_account(uid)
        if len(available_account_list) < mininumNumberOfAccounts:
            try:
                t=threading.Thread(target=target, args=(numberOfAccountCreation,))
                t.start()
                return target
            except BinanceError:
                pass

    def allocated_to_user(self, uid, available_account, user_email, simple_pw, nick_name, profile_url, email_notice, push_notice, notice_token=None):
        deposit_address  = available_account[depositAddressFiled]
        current_datetime = currentDatetime

        private_parmas = asdict(PrivateUserDto(uid, user_email, simple_pw))
        private_parmas.update(available_account)
        public_params = asdict(PublicUserDto(current_datetime, uid, user_email, deposit_address, nick_name, profile_url))
        noti_params   = asdict(NoticeDto(user_email, email_notice, push_notice, notice_token))

        return private_parmas, public_params, noti_params

    def available_account(self, available_account_list, uid):
        try:
            available_account = available_account_list.pop(0)
        except IndexError:
            raise NonAvailableAccount
        return available_account