from decimal import Decimal

from src.application.dto.withdrawal_dto import WithdrawalInputDto, WithdrawalOutputDto
from src.application.repository.withdrawal_repository import WithdrawalRepo
from src.domain.services.withdrawal_domain_service import WithdrawalDomainService
from src.domain.value.filed import userStatusFiled, assetFiled, networkFiled, addressFiled, networkCommissionFiled, orderIDFiled, baseQtyFiled,\
     priceFiled, avgEntryPriceFiled
from src.domain.value.data import eventLoop


class WithdrawalApplicationService:
    def __init__(self, input_dto: WithdrawalInputDto):
        self._input_dto = input_dto

    def get_newset_withdrawal(self, withdrawal_repo, withdrawal_domain, uid):
        withdrawal_list   = withdrawal_repo.find_withdrawal_list()
        newest_withdrawal = eventLoop.run_until_complete(withdrawal_domain.get_newest(withdrawal_list))
        return newest_withdrawal

    def get_newest_order(self, withdrawal_repo, withdrawal_domain, uid, order_id):
        order_list        = withdrawal_repo.find_order_list(order_id)
        newest_order      = eventLoop.run_until_complete(withdrawal_domain.get_newest(order_list))
        return newest_order

    def amt_range(self, withdrawal_domain, uid, base_qty, fund_price, asset):
        asset_value       = Decimal(base_qty) * Decimal(fund_price)
        exchange_rate     = withdrawal_domain.get_usdt_exchange_rate(assetFiled)
        amt_high, amt_low = withdrawal_domain.calculate_withdrawal_amt_range(asset_value, exchange_rate)
        return amt_high, amt_low

    def get_investment_info(self, uid, base_qty, fund_price, avg_entry_price):
        asset_value          = Decimal(base_qty) * Decimal(fund_price)
        investment_principal = Decimal(base_qty) * Decimal(avg_entry_price)
        investment_profit    = asset_value - investment_principal
        return investment_principal, investment_profit

    async def get_withdrawal_price(self, withdrawal_repo, uid, fund_name):
        fund_price      = withdrawal_repo.find_fund_data(fund_name)[priceFiled]
        avg_entry_price = withdrawal_repo.find_balance(fund_name)[avgEntryPriceFiled]
        return fund_price, avg_entry_price

    def create_withdrawal_receipt(self) -> WithdrawalOutputDto:
        uid               = self._input_dto.uid
        withdrawal_domain = WithdrawalDomainService(uid)
        withdrawal_repo   = WithdrawalRepo(uid)
        newest_withdrawal = self.get_newset_withdrawal(withdrawal_repo, withdrawal_domain, uid)
        base_qty          = self.get_newest_order(withdrawal_repo, withdrawal_domain, uid, newest_withdrawal[orderIDFiled])[baseQtyFiled]

        fund_price, avg_entry_price = eventLoop.run_until_complete(self.get_withdrawal_price(withdrawal_repo, uid, self._input_dto.fund_name))

        wd_status  = newest_withdrawal[userStatusFiled]
        wd_asset   = newest_withdrawal[assetFiled]
        wd_network = newest_withdrawal[networkFiled]
        wd_address = newest_withdrawal[addressFiled]
        wd_fee     = newest_withdrawal.get(networkCommissionFiled, 0)

        remaining_secounds = eventLoop.run_until_complete(withdrawal_domain.get_remaining_secound(wd_status))
        amt_high, amt_low = self.amt_range(withdrawal_domain, uid, base_qty, fund_price, wd_asset)
        investment_principal, investment_profit = self.get_investment_info(uid, base_qty, fund_price, avg_entry_price)
        return WithdrawalOutputDto(uid=uid,
                                    status=wd_status,
                                    asset=wd_asset,
                                    network=wd_network,
                                    withdrawal_address=wd_address,
                                    remaining_secounds=remaining_secounds,
                                    expected_amt_high=amt_high,
                                    expected_amt_low=amt_low,
                                    investment_principal=investment_principal,
                                    inbestment_profit=investment_profit,
                                    withdrawal_fee=wd_fee)

    def cancel_withdrawal(self):
        uid               = self._input_dto.uid
        withdrawal_repo   = WithdrawalRepo(uid)
        withdrawal_domain = WithdrawalDomainService(uid)
        newst_withdrawal  = self.get_newset_withdrawal(withdrawal_repo, withdrawal_domain, uid)
        order_id          = newst_withdrawal[orderIDFiled]
        withdrawal_status = newst_withdrawal[userStatusFiled]

        status_params = WithdrawalDomainService(uid).record_cancle_withdrawal(withdrawal_status)
        result = WithdrawalRepo(uid).update_withdrawal_status(order_id, status_params)
        return result
