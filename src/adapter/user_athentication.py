from flask import request
from functools import wraps

from src.application.repository.auth_repository import AuthRepo
from src.domain.value.exceptions import ReqMethodsError

    
def EmailAuth(func):
    @wraps(func)
    def user_auth(*args, **kwargs):
        required_user_email = None
        if request.args.get('user_email') or request.form['user_email']:
            required_user_email = request.args.get('user_email') or request.form['user_email']
        else:
            raise ReqMethodsError
        uid = AuthRepo(required_user_email).find_uid()
        return func(uid, *args, **kwargs)
    return user_auth
