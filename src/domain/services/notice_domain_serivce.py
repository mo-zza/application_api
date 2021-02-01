from src.domain.value.exceptions import NotFound, ZeroDBCustom

class NoticeListDomainService:
    def __init__(self, notice_docs):
        self.notice_docs = notice_docs

    def check_notice_empty(self):
        if self.notice_docs == []:
            raise ZeroDBCustom(self.notice_docs)

    def sorting_notice_list(self):
        notice_list = {}
        self.check_notice_empty()
        for notice_doc in self.notice_docs:
            notice_list[notice_doc.id] = notice_doc.to_dict()
        notice_list = sorted(notice_list.items(), reverse=True)
        return notice_list