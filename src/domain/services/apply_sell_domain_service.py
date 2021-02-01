from decimal import Decimal
from uuid import uuid4

from src.domain.value.exceptions import ZeroBalance, UnFinishOrder

class ApplySellDomainService:
    def __init__(self, uid):
        self.uid = uid

    def get_order_id(self, unfinished_order, user_qty):
        if unfinished_order:
            raise UnFinishOrder('sell')
        if user_qty <= Decimal("0"):
            raise ZeroBalance()
        order_id = str(uuid4())
        return order_id