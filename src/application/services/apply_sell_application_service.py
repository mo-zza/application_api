from dataclasses import asdict

from src.application.repository.sell_repository import SellRepo
from src.application.dto.sell_dto import SellInputDto, SellOutputDto
from src.application.dto.sell_dto import OrderInputDto, WithdrawDto, OrderDto
from src.domain.services.apply_sell_domain_service import ApplySellDomainService
from src.domain.value.data import currentDatetime, eventLoop, koreaDatetime
from src.domain.value.filed import sideSellFiled


class ApplySellApplicationService:
    def __init__(self, input_dto: SellInputDto):
        self._input_dto = input_dto

    async def get_sell_order_info(self, sell_repo, fund_name):
        user_qty             = sell_repo.find_user_balance(fund_name)
        sell_order_snapshots = sell_repo.find_previous_sell_orders(fund_name)
        return user_qty, sell_order_snapshots

    async def build_order_result(self, sell_repo, order_input, withdrawal_input):
        sell_repo.create_order(order_input)
        sell_repo.create_withdrawal(withdrawal_input)
        return 'success'

    def create_order(self) -> SellOutputDto:
        fund_name            = self._input_dto.fund_name
        uid                  = self._input_dto.uid
        sell_repo            = SellRepo(uid)
        
        user_qty, sell_order_snapshots = eventLoop.run_until_complete(self.get_sell_order_info(sell_repo, fund_name))
        unfinished_order   = sell_repo.find_unfinished_order(sell_order_snapshots)
        order_id           = ApplySellDomainService(uid).get_order_id(unfinished_order, user_qty)
        network_commission = sell_repo.find_network_commission(self._input_dto.asset, self._input_dto.network)

        withdrawal_input = WithdrawDto(uid=uid,
                                        order_id=order_id,
                                        address=self._input_dto.address,
                                        asset=self._input_dto.asset,
                                        network=self._input_dto.network,
                                        network_commission=network_commission,
                                        datetime=koreaDatetime,
                                        updated_datetime=koreaDatetime)
                                        
        order_input = OrderDto(uid=uid,
                               order_id=order_id,
                               fund_name=fund_name,
                               side=sideSellFiled,
                               base_qty=str(user_qty),
                               datetime=koreaDatetime,
                               updated_datetime=koreaDatetime)

        order_result = eventLoop.run_until_complete(self.build_order_result(sell_repo, order_input, withdrawal_input))
        return order_result