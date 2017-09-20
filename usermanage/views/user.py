# encoding: utf-8
import json
import sys

from flask import redirect
from flask import render_template
# 引入flask中的必要类和函数
from flask import request
from flask import session
# 导入自定义的模块
from app import app

from usermanage.login_required import login_required
from usermanage.permit_required import permit_required
from utils.loggerutil import logger
from utils.pagelist import PageList
from usermanage.models.user import User

reload(sys)
sys.setdefaultencoding('utf-8')


# 登陆验证
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    user = User.create_by_request(request)
    # 验证用户名和密码
    if user.login():
        session['user'] = user.username
        # 成功则跳转到用户列表
        return redirect('/user/list')
    else:
        # 失败则提示失败信息, 返回登陆页面
        return render_template('usermanage/login.html', error='用户名或密码错误', login_username=user.username)


# 注销登录
@app.route('/user/logout', methods=['GET'])
def logout():
    session.pop('user')
    return redirect('/')


# 获取用户列表
@app.route('/user/list', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def userlist():
    # print from flask import request
    #for x in request.headers:
    #    print x
    #print request.url
    # print request.remote_addr
    params = request.args if request.method == 'GET' else request.form
    _query_username = params.get('query_username', '')
    _query_status = params.getlist('query_status')
    _page_size = params.get('pageSize', '')
    _page_num = params.get('pageNum', 1)
    _total = User.fetch_all(count=True, username=_query_username, status=_query_status)

    # 生成pagelist对象
    _pagelist, _offset = PageList.create_pagelist(_page_num, _page_size, _total)
    # 获取所有用户
    _rst = User.fetch_all(username=_query_username, status=_query_status,
                                 offset=_offset, limit=_pagelist.pageSize)
    # 结果设置为pagelist的contents属性
    _pagelist.set_contents(_rst)
    # 响应页面
    return render_template('usermanage/users.html', pageList=_pagelist,
                           query_username=_query_username, query_status=_query_status)


# 添加用户
@app.route('/user/add', methods=['POST'])
@login_required
def adduser():
    user = User.create_by_request(request)
    # 检查用户提交的数据
    ok, result = user.validate_add()
    
    # 如果检查通过则添加到文件中
    if ok:
        if user.create():
            ok = True
            result = '添加成功'
        else:
            ok = False
            result = '添加失败'
            
    return json.dumps({'ok': ok, 'result': result})


# 更新用户
@app.route('/user/update', methods=['POST'])
@login_required
def updateuser():
    _uid = request.form.get('uid', '')
    _ouser = User.get_by_keys(uid=_uid)
    if _ouser is None:
        logger.warning('Cannot find user with uid=%s', _uid)
        ok, result = False, '用户信息不存在'
    else:
       
        _nuser = User.create_by_request(request)
        # 检查用户提交的数据
        ok, result = _nuser.validate_modify()
        # 如果检查通过则添加到DB
        if ok:
            if _nuser.update():
                ok = True
                result = '更新成功'
            else:
                ok = False
                result = '更新失败'
    print ok, result
    return json.dumps({'ok': ok, 'result': result})


# 删除用户信息
@app.route('/user/delete')
@login_required
def deleteuser():
    _uid = request.args.get('uid', '')
    ok, result = User.delete(_uid)
    if not ok:
        result = "用户删除失败"
    return json.dumps({'ok': ok, 'result': result})
