# encoding:utf-8

# from flask import session
# from flask import abort
from flask import render_template
from functools import wraps


def permit_required(permitid):
    def __perm(func):
        @wraps(func)
        def __wapper(*args, **kwargs):
            # permitlist,从数据库中获取的权限值
            # permitlist = models.Permit.getbykey(username=session.get('user'))
            permitlist = ['20010', '20011']
            if permitid in permitlist:
                rtn = func(*args, **kwargs)
            else:
                return render_template('nopermit.html')
            # return redirect('/')
            return rtn
        return __wapper
    return __perm
