# encoding: utf-8
from flask import session
from flask import redirect
from functools import wraps


# 登录验证装饰器
def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper
