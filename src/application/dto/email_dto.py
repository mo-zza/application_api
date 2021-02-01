from dataclasses import dataclass


@dataclass
class EmailInputDto:
    user_email: str
    uid: str

@dataclass
class EmailOutputDto:
    otp: str
    hash_otp: str

@dataclass
class CheckOTPInputDto:
    uid: str
    user_email: str
    req_otp: str

@dataclass
class CheckOTPOutputDto:
    status: str
        
@dataclass
class CheckEmailInputDto:
    req_otp: str
    crypto_otp: str
    user_status: str
    false_count: int
    uid: str
    repo: any

@dataclass
class EmailCountDto:
    count: int

@dataclass
class EmailDto:
    otp: str
    count: int = 0

@dataclass
class UserLock:
    status: str