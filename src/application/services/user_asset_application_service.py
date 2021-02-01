from src.application.repository.user_repository import UserRepo
from src.application.repository.sell_repository import SellRepo
from src.application.dto.users_dto import SimpleInputDto, AssetOutputDto
from src.domain.services.user_asset_domain_service import UserAssetDomainService
from src.domain.value.data import eventLoop
from src.infrastructure.multi_thread import ThreadProcess
from src.domain.value.filed import btcFiled, btcNetworkFiled, usdtFiled, usdtNetworkFiled

class UserAssetApplicationService:
    def __init__(self, input_dto: SimpleInputDto):
        self._input_dto = input_dto

    def get_user_asset_data(self, user_repo, asset_domain):
        current_price               = user_repo.find_current_price()
        latest_completes_order_time = asset_domain.get_latest_completed_sell_order_time()
        return current_price, latest_completes_order_time

    async def get_all_network_commistion(self, sell_repo):
        btc_network_commission     = sell_repo.find_network_commission(btcFiled, btcNetworkFiled)
        usdt_network_commission    = sell_repo.find_network_commission(usdtFiled, usdtNetworkFiled)
        return float(btc_network_commission), float(usdt_network_commission)

    async def get_asset_output_dto(self, sell_repo, asset_domain, latest_completes_order_time, current_price) -> AssetOutputDto:
        current_buy_list           = asset_domain.get_current_buy_order(latest_completes_order_time)
        total_base_qty             = eventLoop.run_until_complete(asset_domain.get_total_base_qty(current_buy_list))
        total_asset                = eventLoop.run_until_complete(asset_domain.get_total_asset(current_price, current_buy_list))
        yield_return, total_return = eventLoop.run_until_complete(asset_domain.get_yield_asset(total_asset, total_base_qty))
        btc_fee, usdt_fee          = eventLoop.run_until_complete(self.get_all_network_commistion(sell_repo))
        return AssetOutputDto(total_base_qty=total_base_qty,
                            total_return=total_return,
                            yield_return=yield_return,
                            total_asset=total_asset,
                            btc_withdrawal_fee=btc_fee,
                            usdt_withdrawal_fee=usdt_fee)

    def user_asset(self):
        uid          = self._input_dto.uid
        user_repo    = UserRepo(uid)
        sell_repo    = SellRepo(uid)
        asset_domain = UserAssetDomainService(uid, user_repo)

        current_price, latest_completes_order_time = self.get_user_asset_data(user_repo, asset_domain)
        output_dto = eventLoop.run_until_complete(self.get_asset_output_dto(sell_repo=sell_repo,
                                                                            asset_domain=asset_domain,
                                                                            latest_completes_order_time=latest_completes_order_time,
                                                                            current_price=current_price))
        return output_dto