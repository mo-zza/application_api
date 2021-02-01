from dataclasses import dataclass, field


@dataclass
class ChangePw:
    uid: str
    simple_pw: str

@dataclass
class Users:
    uid: str
    simple_pw: str = field(compare=False)

class UserEmail:
    def __init__(self, user_email: str):
        if isinstance(user_email, str) == False:
            raise TypeError('user email must be string')
        self.user_email = user_email

@dataclass
class SimplePw:
    def __init__(self, simple_pw: str):
        if 'argon' not in simple_pw:
            raise ValueError('Please enryption password.')
        self.simple_pw = simple_pw

class AvailableSubAccountList:
    def __init__(self, available_accounts):
        sub_account_list = [available_account.to_dict() for available_account in available_accounts]
        self.sub_account_list = sub_account_list