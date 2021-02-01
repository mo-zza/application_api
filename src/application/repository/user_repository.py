from dataclasses import asdict

from src import firestore
from src.application.dto.users_dto import ProfileDto
from src.domain.value.collection import usersCol, subAccountsCol, fundCol, zlbUsdtFundCol, issueHistoryCol, \
    orderCol, userPrivateCol, noticeCol, depositCol, withdrawalCol, exchangeCol
from src.domain.value.filed import subAccountOccupiedFiled, defaultSubAccountOccupiedFiled, subAccountIDFiled,\
     datetimeFiled, priceFiled, userStatusFiled, simplePwFiled, completedFiled
from src.domain.entities.users_entity import AvailableSubAccountList
from src.domain.value.exceptions import NotFound, VerifyPassword, ZeroDBCustom, AlreadyUser


class UserRepo:
    def __init__(self, uid):
        self.uid       = uid
        self.firestore = firestore

    def find_user_display_name(self, email):
        try:
            display_name = self.firestore.get_auth_user(email).display_name
            return display_name
        except:
            NotFound('Nick name')

    def find_user_profile_url(self, email):
        try:
            profile_url = self.firestore.get_auth_user(email).photo_url
            return profile_url
        except:
            NotFound('profile url')

    def save_user_profile(self, profile_dto: ProfileDto):
        try:
            save_profile_result = self.firestore.update_document(usersCol, self.uid, asdict(profile_dto))
            return save_profile_result
        except:
            NotFound('profile')

    def find_user_status(self):
        try:
            user_info = self.firestore.read_document(usersCol, self.uid).to_dict()
            return user_info[userStatusFiled]
        except:
            raise NotFound('user status.')

    def save_account(self, sub_id, account_params):
        self.firestore.db.collection(subAccountsCol).document(sub_id).set(account_params)        
        return account_params

    def update_user_info(self, params):
        try:
            self.firestore.update_document(usersCol, self.uid, params)
            return 'success'
        except:
            raise NotFound('nick name')
    
    def find_available_sub_account_list(self):
        available_accounts     = self.firestore.query_collection(subAccountsCol, subAccountOccupiedFiled, '==', defaultSubAccountOccupiedFiled)
        available_account_list = AvailableSubAccountList(available_accounts).sub_account_list
        return available_account_list

    def save_user_initial_set(self, available_account, uid, private_user_params, public_user_params, notice_params):
        subaccount_id = available_account[subAccountIDFiled]
        self.firestore.update_document(subAccountsCol, subaccount_id, {subAccountOccupiedFiled : True})
        self.firestore.create_document(userPrivateCol, uid, private_user_params)
        self.firestore.create_document(usersCol, uid, public_user_params)
        self.firestore.create_document(noticeCol, uid, notice_params)
        return subaccount_id

    def find_current_price(self):
        fund_data     = self.firestore.query_one_sub_document_data(fundCol, zlbUsdtFundCol, issueHistoryCol, datetimeFiled)
        current_price = fund_data[0].to_dict()[priceFiled]
        return current_price

    def find_completed_order(self):
        try:
            complete_list             = self.firestore.query_sub_collection(usersCol, self.uid, orderCol, userStatusFiled, '==', completedFiled)
            complete_info_list        = [complete_info.to_dict() for complete_info in complete_list]
            sorted_complete_info_list = sorted(complete_info_list, key=lambda complete_info_list: (complete_info_list[datetimeFiled]), reverse=True)
            return sorted_complete_info_list
        except:
            return None

    def find_current_order(self, sell_date):
        order_data_list   = self.firestore.query_sub_collection(usersCol, self.uid, orderCol, datetimeFiled, '>', sell_date)
        order_list        = [order_data.to_dict() for order_data in order_data_list]
        sorted_order_list = sorted(order_list, key=lambda order_list: (order_list[datetimeFiled]), reverse=True)
        return sorted_order_list

    def find_all_order(self):
        order_data_list = self.firestore.read_sub_collection(usersCol, self.uid, orderCol)
        if order_data_list == []:
            raise ZeroDBCustom(order_data_list)
        else:
            order_list        = [order_data.to_dict() for order_data in order_data_list]
            sorted_order_list = sorted(order_list, key=lambda order_list: (order_list[datetimeFiled]), reverse=True)
            return sorted_order_list

    def find_user_diposit_list(self):
        deposits_list = self.firestore.read_sub_collection(usersCol, self.uid, depositCol)
        return deposits_list

    def find_user_withdrawal_list(self):
        withdrawals_list = self.firestore.read_sub_collection(usersCol, self.uid, withdrawalCol)
        return withdrawals_list

    def find_user_exchange_list(self):
        exchanges_list = firestore.read_sub_collection(usersCol, self.uid, exchangeCol)
        return exchanges_list

    def find_newly_current_price(self, lately_buy_date):
        newly_issue_list      = self.firestore.query_sub_collection(fundCol, zlbUsdtFundCol, issueHistoryCol, datetimeFiled, '>', lately_buy_date[datetimeFiled])
        newly_issue_data_list = [newly_issue_data.to_dict() for newly_issue_data in newly_issue_list]
        return newly_issue_data_list

    async def find_simple_pw(self):
        try:
            user_private_info = self.firestore.read_document(userPrivateCol, self.uid).to_dict()
            simple_pw         = user_private_info[simplePwFiled]
        except:
            raise ZeroDBCustom("")
        return simple_pw
        
    def update_simple_pw(self, params):
        try:
            self.firestore.update_document(userPrivateCol, self.uid, params)
            return 'success'
        except:
            raise VerifyPassword