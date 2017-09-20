#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import json
import math
from functools import wraps

# 引入flask中的必要类和函数
from flask import Flask              #创建Flask APP对象
from flask import request            #用于获取用户提交的数据
from flask import render_template    #加载模板
from flask import redirect           #重定向到其他url
from flask import session 

# 导入自定义的模块
from website import models
import gconf


# 创建一个Flask app
# Flask需要根据传递的参数去寻找templates, static等目录的位置
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX aHH!sajmN]LWX/,?RT'

# 登录验证装饰器
def login_required(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args,**kwargs)
        return rtn
    return wapper

# homepage
# 定义路由, 如果以GET方式访问url地址为/则由index函数处理
@app.route('/')
def index():
    time.sleep(5)
    # 如果已登录状态，直接跳转到登录后url
    #app.logger.error('A value for debugging')
    if session.get('user') is not None:
        return redirect('/user/list')
    #print session
    #print session.get('user')
    # 返回templates目录下的login.html模板中的内容
    return render_template('login.html')


## ========================================== /user/ ========================================##

# 登陆验证
# 定义路由, 若以GET、POST方式提交请求到url地址/login/则有login函数处理
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    params = request.args if request.method == 'GET' else request.form
    user = models.User(params)
    
    # 验证用户名和密码
    #if models.validate_user_login(username, password):
    if user.login():
        session['user']=user.username
        # 成功则显示所有用户的信息列表
        return redirect('/user/list')
    else:
        # 失败则提示用户失败, 依然返回登陆页面
        return render_template('login.html', error='用户名或密码错误', login_username=user.username)

# 注销登录
@app.route('/user/logout')
def logout():
    session.pop('user')
    return redirect('/')



# 获取用户列表
# 定义路由, 如果以GET方式访问url地址为/users/则由users函数处理
@app.route('/user/list', methods=['GET', 'POST'])
@login_required
def userlist():
    params = request.args if request.method == 'GET' else request.form
    _query_username = params.get('query_username', '')
    _query_status = params.getlist('query_status')
    #_query_xxx = params.get('query_xxx', '')
    _total = models.User.fetch_all(count=True, username=_query_username, status=_query_status)
    _page_size = params.get('pageSize', gconf.PAGESIZE)
    _page_num = params.get('pageNum', 1)
    # 分页大小
    _page_size = int(_page_size) if str(_page_size).isdigit() else gconf.PAGESIZE
    _page_size = gconf.PAGESIZE if int(_page_size) < 5 or int(_page_size) >50 else _page_size
    # 总页数
    _max_page_num = int(math.ceil( _total *1.0 / _page_size))    
    _page_num = int(_page_num) if str(_page_num).isdigit() else 1
    _page_num = 1 if _page_num < 1 or _page_num > _max_page_num else _page_num
    # DB偏移量
    _offset = ( _page_num -1 ) * _page_size
    # 结束页码
    _end_page_num = _page_num + 2
    _end_page_num = _end_page_num if _end_page_num < _max_page_num and _max_page_num > 5 else _max_page_num
    _end_page_num = 5 if _max_page_num > 5 and _end_page_num < 5 else _end_page_num
    # 起始页码
    _start_page_num = _end_page_num -4
    _start_page_num = 1 if _end_page_num <=5 else  _start_page_num 

    
    # 获取所有用户
    _users = models.User.fetch_all(username=_query_username, status=_query_status, offset=_offset, limit=_page_size)
    return render_template('users.html', users=_users, query_username=_query_username,\
                           startPageNum=_start_page_num, endPageNum=_end_page_num,\
                           pageNum=_page_num, maxPageNum=_max_page_num, \
                           pageSize=_page_size ,query_status=_query_status)


# 添加用户
@app.route('/user/add', methods=['POST'])
@login_required
def addUser():
    params = request.args if request.method == 'GET' else request.form
    user = models.User(params)

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
            
    return json.dumps({'ok':ok,'result':result})


# 更新用户
@app.route('/user/update', methods=['POST'])
@login_required
def updateUser():
    _uid = request.form.get('uid', '')
    _ouser = models.User.get_by_keys(uid=_uid)
    if _ouser is None:
        ok,result = False,'用户信息不存在'
    else:
       
        _nuser = models.User(request.form)
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

    return json.dumps({'ok':ok,'result':result})

# 删除用户信息
@app.route('/user/delete')
@login_required
def deleteUser():
    _uid = request.args.get('uid', '')
    ok,result = models.User.delete(_uid)
    if not ok:
        result = "用户删除失败"
    return json.dumps({'ok':ok,'result':result})

## ========================================== end /user/ ========================================##


## ========================================== /infoserver/ ========================================##
# 获取列表
@app.route('/infoserver/list', methods=['GET', 'POST'])
@login_required
def getInfoServer():
    params = request.args if request.method == 'GET' else request.form
    _query_sn = params.get('query_sn', '')
    _query_sort = params.get('query_sort', '')
    _page_size = params.get('pageSize', gconf.PAGESIZE)
    _page_num = params.get('pageNum', 1)
    _total = models.InfoServer.fetch_all(count=True, sn=_query_sn)
    # 分页大小
    _page_size = int(_page_size) if str(_page_size).isdigit() else gconf.PAGESIZE
    _page_size = gconf.PAGESIZE if int(_page_size) < 5 or int(_page_size) >50 else _page_size
    # 总页数
    _max_page_num = int(math.ceil( _total *1.0 / _page_size))    
    _page_num = int(_page_num) if str(_page_num).isdigit() else 1
    _page_num = 1 if _page_num < 1 or _page_num > _max_page_num else _page_num
    # DB偏移量
    _offset = ( _page_num -1 ) * _page_size
    # 结束页码
    _end_page_num = _page_num + 2
    _end_page_num = _end_page_num if _end_page_num < _max_page_num and _max_page_num > 5 else _max_page_num
    _end_page_num = 5 if _max_page_num > 5 and _end_page_num < 5 else _end_page_num
    # 起始页码
    _start_page_num = _end_page_num -4
    _start_page_num = 1 if _end_page_num <=5 else  _start_page_num 

    
    # 获取所有server
    _rst = models.InfoServer.fetch_all(sn=_query_sn, sort=_query_sort, offset=_offset, limit=_page_size)
    #print _rst
    return render_template('infoserver.html', infoserver=_rst, query_sn=_query_sn,\
                           startPageNum=_start_page_num, endPageNum=_end_page_num,\
                           pageNum=_page_num, maxPageNum=_max_page_num, \
                           pageSize=_page_size, query_sort=_query_sort)


# 添加信息
@app.route('/infoserver/add', methods=['POST'])
@login_required
def addInfoServer():
    params = request.args if request.method == 'GET' else request.form
    _infoserver = models.InfoServer(params)

    # 检查用户提交的数据
    ok, result = _infoserver.validate_add()
    
    # 如果检查通过则添加到文件中
    if ok:
        if _infoserver.create():
            ok = True
            result = '添加成功'
        else:
            ok = False
            result = '添加失败'
            
    return json.dumps({'ok':ok,'result':result})


# 更新信息
@app.route('/infoserver/update', methods=['POST'])
@login_required
def updateInfoServer():
    _infoserver = models.InfoServer(request.form)
       
    # 检查用户提交的数据
    ok, result = _infoserver.validate_modify()
    # 如果检查通过则添加到DB
    if ok:
        if _infoserver.update():
            ok = True
            result = '更新成功'
        else:
            ok = False
            result = '更新失败'

    return json.dumps({'ok':ok,'result':result})

## ========================================== end /infoserver/ ========================================##



## ========================================== end /machineroom/ ========================================##
# 机房列表
@app.route('/machineroom/list', methods=['GET', 'POST'])
@login_required
def machine_rooms():
    _machine_rooms = models.get_machine_rooms()
    return json.dumps(_machine_rooms)










