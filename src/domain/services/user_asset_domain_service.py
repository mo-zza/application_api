from decimal import Decimal

from src.application.repository.user_repository import UserRepo
from src.domain.value.filed import datetimeFiled, sideFiled, sideBuyFild, baseQtyFiled, priceFiled, sideSellFiled, quoteQtyFiled
from src.domain.value.exceptions import ZeroAsset

class UserAssetDomainService:
    def __init__(self, uid, user_repo: UserRepo):
        self.uid = uid
        self._user_repo = user_repo

    def find_sell_order(self, completed_order_list):
        sell_order_list = [completed_order[datetimeFiled] for completed_order in completed_order_list if completed_order[sideFiled] == sideSellFiled]
        return sell_order_list

    def select_last_order_time(self, last_order_datettime_list):
        if last_order_datettime_list == []:
            return None
        else:
            return last_order_datettime_list[0]

    def get_latest_completed_sell_order_time(self) -> dict:
        completed_order_list = self._user_repo.find_completed_order()
        if completed_order_list == None:
            raise ZeroAsset("User doess't have any Asset.")
        else:
            sell_order_datetime_list = self.find_sell_order(completed_order_list)
            last_order_time = self.select_last_order_time(sell_order_datetime_list)
            return last_order_time

    def get_current_buy_order(self, last_sell_time) -> list:
        if last_sell_time == None:
            current_order_list = self._user_repo.find_all_order()
        else:
            current_order_list = self._user_repo.find_current_order(last_sell_time)
        current_buy_list = list(filter(lambda i: i[sideFiled] == sideBuyFild, current_order_list))
        return current_buy_list

    async def get_total_asset(self, current_price, buy_list):
        completed_assets = [Decimal(buy_data[baseQtyFiled]) for buy_data in buy_list if buy_data[baseQtyFiled] != ""]
        receiving_assets = [Decimal(buy_data[quoteQtyFiled]) for buy_data in buy_list if buy_data[baseQtyFiled] == ""]
        if completed_assets == [] and receiving_assets == []:
            qoute_list  = [Decimal(buy_data[quoteQtyFiled]) for buy_data in buy_list]
            total_asset = Decimal(sum(qoute_list))
        else:
            total_asset = Decimal(sum(completed_assets)) * Decimal(current_price) + Decimal(sum(receiving_assets))
        return float(total_asset)

    async def get_total_base_qty(self, buy_list):
        base_qty = [Decimal(buy_data[quoteQtyFiled]) for buy_data in buy_list]
        return float(sum(base_qty))

    async def get_yield_asset(self, total_asset, total_base_qty):
        if total_asset == 0 and total_base_qty == 0:
            return 0.0, 0.0
        total_yield  = ((Decimal(total_asset) / Decimal(total_base_qty)) - Decimal(1)) * Decimal(100)
        total_return = Decimal(total_asset) - Decimal(total_base_qty)
        return float(total_yield), float(total_return)