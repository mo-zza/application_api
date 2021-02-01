class CustomNotFound(Exception):
    '''
    커스텀된 에러. 에러 메세지 직접 발생 가능
    '''
    def __init__(self, desciprtion):
        self.code = 404
        self.description = desciprtion

class UnAuthenticationError(Exception):
    '''
    이메일 인증이 되지 않은 사용자
    '''
    code = 401
    description = 'The un-authentication email.'

class ServerError(Exception):
    '''
    서버 에러. 로직상 문제가 생겼을 때, 발생
    '''
    def __init__(self, description):
        self.code = 500
        self.description = description

class VerifyTokenError(Exception):
    '''
    jwt token error
    '''
    code = 401
    description = 'Token is Dead.'

class UnFinishOrder(Exception):
    '''
    주문 및 요청이 아직 처리가 되지 않았을 때 발생
    '''
    def __init__(self, desciprtion):
        self.code = 500
        self.description = f"The user's previos {desciprtion} order is not finished yet."

class ZeroBalance(Exception):
    '''
    유저릐 자산이 없을 때
    '''
    code = 403
    description = 'The user balance is not sufficient.'

class LockedUser(Exception):
    '''
    사용 불가 유저
    '''
    code = 401
    description = 'The user is Locked.'

class VerifyPassword(Exception):
    '''
    패스워드 불일치
    '''
    code = 401
    description = 'Password is not verify.'

class ZeroFundAsset(Exception):
    '''
    펀드 자산 없을 떄, 
    '''
    def __init__(self, description):
        self.code = 403
        self.description = f"issue history's {description} doesn't have 'datetime' or 'price' field."

class ZeroFunding(Exception):
    '''
    펀딩 내역이 없을 떄,
    '''
    def __init__(self, description):
        self.code = 403
        self.description = f"funding history's {description} doesn't have 'datetime', 'cum_issue_qty', 'price' field."

class ZeroRecord(Exception):
    '''
    내역이 없을 때,
    '''
    def __init__(self, description):
        self.code = 403
        self.description = f"There isn't {description} record."

class ZeroAsset(Exception):
    '''
    asset이 없을 떄
    '''
    def __init__(self, description):
        self.code = 404
        self.description = description

class ReqMethodsError(Exception):
    '''
    메소드 에러
    '''
    code = 405
    description = f'Method Error'

class VerifyOTP(Exception):
    '''
    OTP가 틀렸을 때
    '''
    code = 401
    description = 'OTP is un verified'

class NotFound(Exception):
    '''
    repository가 찾지 못했을 때,
    '''
    def __init__(self, description):
        self.code = 404
        self.description = f'Not Found {description}'

class InsuffiientError(Exception):
    '''
    Fund insuffiient error
    '''
    code = 404
    description = "issue record(s) are insuffinient."

class ZeroDBCustom(Exception):
    def __init__(self, description):
        self.code = 200
        self.description = description

class AlreadyUser(Exception):
    code = 403
    description = "There is already user."

class NonAvailableAccount(Exception):
    code = 500
    description = "There is not have available account"

class BinanceError(Exception):
    code = 500
    description = "Binance Error"