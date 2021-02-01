from src.application.repository.user_repository import UserRepo
from src.application.dto.users_dto import SimpleInputDto, SimpleOutPutDto
from src.domain.services.user_asset_domain_service import UserAssetDomainService
from src.domain.services.user_chart_domain_service import UserChartDomainService
from src.infrastructure.multi_thread import ThreadProcess

class UserChartApplicationChart:
    def __init__(self, input_dto: SimpleInputDto):
        self._input_dto = input_dto

    def get_newst_buy_list(self, uid, user_repo):
        asset_domain               = UserAssetDomainService(uid, user_repo)
        latest_completed_sell_time = asset_domain.get_latest_completed_sell_order_time()
        newst_buy_list             = asset_domain.get_current_buy_order(latest_completed_sell_time)
        return newst_buy_list

    def newet_current_list(self, uid, user_repo):
        newst_buy_list        = self.get_newst_buy_list(uid, user_repo)
        newst_fund_issue_list = user_repo.find_newly_current_price(newst_buy_list[-1])
        newet_current_list    = UserChartDomainService().get_newly_price_list(newst_buy_list, newst_fund_issue_list)
        return newet_current_list

    def user_chart(self):
        uid       = self._input_dto.uid
        user_repo = UserRepo(uid)

        newst_current_list = self.newet_current_list(uid, user_repo)
        user_chart         = UserChartDomainService().get_chart_data(newst_current_list)
        return user_chart