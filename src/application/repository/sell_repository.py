from decimal import Decimal
from dataclasses import asdict

from src import firestore
from src.application.dto.sell_dto import OrderDto, WithdrawDto
from src.domain.value.collection import usersCol, orderCol, withdrawalCol, policiesCol
from src.domain.value.document import withdrawalDoc
from src.domain.value.filed import userIDFiled, sideFiled, qtyFiled, fundNameFiled, sideSellFiled, datetimeFiled,\
    descQueryFiled, userStatusFiled, newStatusFiled, receivedStatusFiled, withdrawalFeeFiled
from src.domain.value.exceptions import NotFound, ZeroBalance


class SellRepo:
    def __init__(self, uid):
        self.uid       = uid
        self.firestore = firestore

    def find_user_balance(self, fund_name):
        user_ref = self.firestore.read_ordered_sub_documents(usersCol, self.uid, fund_name, datetimeFiled, descQueryFiled, 1)
        try:
            user_qty = Decimal(user_ref[0].to_dict()[qtyFiled])
        except (IndexError, AttributeError, KeyError):
            user_qty = Decimal("0")
        return user_qty

    def find_previous_sell_orders(self, fund_name):
        orders      = self.firestore.db.collection(f'{usersCol}/{self.uid}/{orderCol}').where(userIDFiled,"==",self.uid)
        sell_orders = orders.where(fundNameFiled, "==", fund_name).where(sideFiled,"==",sideSellFiled).get()
        return sell_orders

    def find_unfinished_order(self, sell_order_snapshots):
        for snapshot in sell_order_snapshots:
            order = snapshot.to_dict()
            if order[userStatusFiled] in newStatusFiled or order[userStatusFiled] in receivedStatusFiled:
                return order

    def find_network_commission(self, asset, network):
        try:
            network_doc        = self.firestore.read_document(policiesCol, withdrawalDoc)
            network_data       = network_doc.to_dict()
            network_commission = network_data[asset][network][withdrawalFeeFiled]
            return network_commission
        except:
            raise NotFound('withdrawal fee')
            
    def create_order(self, order_input: OrderDto):
        order = asdict(order_input)
        self.firestore.create_sub_document(usersCol, self.uid, orderCol, order_input.order_id, order)
        return order

    def create_withdrawal(self, withdrawal_input: WithdrawDto):
        withdrawal = asdict(withdrawal_input)
        self.firestore.create_sub_document(usersCol, self.uid, withdrawalCol, withdrawal_input.order_id, withdrawal)
        return withdrawal