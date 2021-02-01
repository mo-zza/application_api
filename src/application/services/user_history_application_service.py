from src.application.repository.user_repository import UserRepo
from src.application.dto.users_dto import SimpleInputDto, SimpleOutPutDto
from src.domain.services.user_history_domain_service import UserHistoryDomainService
from src.domain.value.filed import assetFiled, datetimeFiled, symbolFiled, assetQtyFiled, baseQtyFiled, qtyFiled, sideFiled, sideBuyFild, sideSellFiled
from src.domain.value.data import eventLoop

class UserHistoryApplicationService:
    def __init__(self, input_dto: SimpleInputDto):
        self._input_dto = input_dto

    async def get_user_history_datas(self, user_repo):
        deposit_datas    = user_repo.find_user_diposit_list()
        withdrawal_datas = user_repo.find_user_withdrawal_list()
        exchange_datas   = user_repo.find_user_exchange_list()
        return deposit_datas, withdrawal_datas, exchange_datas

    async def get_order_list(self, history_domain, deposit_datas, withdrawal_datas, exchange_datas):
        deposits_list    = history_domain.build_history_res(deposit_datas, '입금', assetFiled, qtyFiled)
        withdrawals_list = history_domain.build_history_res(withdrawal_datas, '출금', assetFiled, assetQtyFiled)
        exchanges_list   = history_domain.build_history_res(exchange_datas, '환전', symbolFiled, baseQtyFiled)
        return deposits_list, withdrawals_list, exchanges_list
    
    def user_history(self):
        uid            = self._input_dto.uid
        user_repo      = UserRepo(uid)
        history_domain = UserHistoryDomainService()

        deposit_datas, withdrawal_datas, exchange_datas = eventLoop.run_until_complete(self.get_user_history_datas(user_repo))
        deposits_list, withdrawals_list, exchanges_list = \
            eventLoop.run_until_complete(self.get_order_list(history_domain, deposit_datas, withdrawal_datas, exchange_datas))

        extend_all_list = deposits_list + withdrawals_list + exchanges_list
        history_list    = sorted(extend_all_list, key=lambda extend_all_list: (extend_all_list[datetimeFiled]), reverse=True)
        return history_list