from src import firestore
from src.domain.value.collection import noticeCol, noticeListCol
from src.domain.value.exceptions import NotFound

class NoticeRepo:
    def __init__(self):
        self.firestore = firestore

    def update_notice(self, uid, notice_params):
        try:
            firestore.update_document(noticeCol, uid, notice_params)
            return 'success'
        except:
            raise NotFound('notice')

    def find_notice_list(self, uid):
        notice_docs = self.firestore.read_sub_collection(noticeCol, uid, noticeListCol)
        return notice_docs