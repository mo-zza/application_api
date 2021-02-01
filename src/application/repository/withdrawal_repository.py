from dataclasses import asdict

from src import firestore
from src.domain.value.collection import usersCol, withdrawalCol, orderCol, fundCol
from src.domain.value.filed import datetimeFiled, orderIDFiled
from src.domain.value.exceptions import NotFound


class WithdrawalRepo:
    def __init__(self, uid):
        self.uid       = uid
        self.firestore = firestore

    def find_withdrawal_list(self):
        withdrawal_list = self.firestore.query_one_sub_document_data(usersCol, self.uid, withdrawalCol, datetimeFiled)
        return withdrawal_list

    def find_order_list(self, order_id):
        order_query = self.firestore.db.collection_group(orderCol).where(orderIDFiled, '==', order_id)
        order_list  = list(order_query.stream())
        return order_list
    
    def find_fund_data(self, fund_name):
        try:
            fund_data = self.firestore.read_document(fundCol, fund_name).to_dict()
            print(fund_data)
            return fund_data
        except:
            raise NotFound('fund data')

    def find_balance(self, fund_name):
        balance_list = self.firestore.query_one_sub_document_data(usersCol, self.uid, fund_name, datetimeFiled)
        balance      = balance_list[0].to_dict()
        return balance

    def update_withdrawal_status(self, order_id, params):
        self.firestore.update_document(f'{usersCol}/{self.uid}/{withdrawalCol}', order_id, asdict(params))
        self.firestore.update_document(f'{usersCol}/{self.uid}/{orderCol}', order_id, asdict(params))
        return 'success'