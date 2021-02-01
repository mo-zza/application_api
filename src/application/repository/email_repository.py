from src import firestore
from src.domain.value.collection import otpCol, usersCol
from src.domain.value.filed import lockStatusFiled
from src.domain.value.exceptions import NotFound, ServerError


class EmailRepo:
    def __init__(self, uid: str) -> None:
        self.firestore = firestore
        self.uid       = uid

    def save_otp(self, email_params):
        try:
            self.firestore.create_document(otpCol, self.uid, email_params)
        except:
            raise NotFound('otp')
        return
    
    def find_otp(self):
        try:
            otp = self.firestore.read_document(otpCol, self.uid).to_dict()['otp']
        except:
            raise NotFound('OTP')
        return otp

    def find_otp_info(self):
        try:
            otp_info = self.firestore.read_document(otpCol, self.uid).to_dict()
            return otp_info['otp'], otp_info['count']
        except:
            raise NotFound('OTP')

    def find_user_status(self):
        try:
            user_info = self.firestore.read_document(usersCol, self.uid).to_dict()
            return user_info['status']
        except:
            raise NotFound('user status.')

    def update_user_status(self, params):
        try:
            self.firestore.update_document(usersCol, self.uid, params)
        except:
            raise ServerError('Update Failed')

    def update_false_count(self, params):
        try:
            self.firestore.update_document(otpCol, self.uid, params)
        except:
            raise ServerError('Update Failed')