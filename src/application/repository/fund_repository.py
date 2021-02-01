from src import firestore
from src.domain.value.collection import fundCol, issueHistoryCol, fundingHistoryCol, usersCol, reportHistoryCol
from src.domain.value.filed import datetimeFiled
from src.domain.value.exceptions import NotFound


class FundRepo:
    def __init__(self):
        self.firestore = firestore

    def find_fund_issue_history(self, fund_name):
        try:
            issue_list = self.firestore.read_sub_collection(fundCol, fund_name, issueHistoryCol)
            return issue_list
        except:
            raise NotFound('issue list.')

    def find_funding_history(self, fund_name):
        try:
            funding_list = self.firestore.read_sub_collection(fundCol, fund_name, fundingHistoryCol)
            return funding_list
        except:
            raise NotFound('fund list.')

    def find_user_fund_history(self, uid, fund_name):
        try:
            user_funding_history = self.firestore.read_ordered_documents(f'{usersCol}/{uid}/{fund_name}', limit=1)
            return user_funding_history
        except:
            raise NotFound('user funding hitsory.')

    def find_fund_issue_list_order_datetime(self, fund_name):
        try:
            issue_list = self.firestore.query_sub_document_data(fundCol, fund_name, issueHistoryCol, datetimeFiled)
            return issue_list
        except:
            raise NotFound("issue list with datetimeFiled")

    def find_report_list_order_datetime(self, fund_name):
        try:
            report_list = self.firestore.query_sub_document_data(fundCol, fund_name, reportHistoryCol, datetimeFiled)
            return report_list
        except:
            raise NotFound("report list with datetimeFiled")