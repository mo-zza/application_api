import jwt
import time

class JwtToken:
    keep_alive_time = 3600
   
    @staticmethod
    def create_token(user):
        current_time = time.time()
        expiration_time = current_time + JwtToken.keep_alive_time
        token = jwt.encode({'iat' : current_time, 'exp' : expiration_time, 'aud' : user}, 'example secret', algorithm="HS256").decode("UTF-8")
        return token