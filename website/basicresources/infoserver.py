# encoding: utf-8
# 导入系统模块
import json
import sys

from flask import render_template  # 加载模板
from flask import request  # 用于获取用户提交的数据
# 引入flask中的必要类和函数
from app import app

from usermanage.login_required import login_required
from utils.pagelist import PageList
# 导入自定义的模块
from website import models

reload(sys)
sys.setdefaultencoding('utf-8')


# 获取列表
@app.route('/infoserver/list', methods=['GET', 'POST'])
@login_required
def getinfoserver():
    params = request.args if request.method == 'GET' else request.form
    _query_sn = params.get('query_sn', '')
    _query_sort = params.get('query_sort', '')
    _page_size = params.get('pageSize', '')
    _page_num = params.get('pageNum', 1)
    _total = models.InfoServer.fetch_all(count=True, sn=_query_sn)

    _pagelist, _offset = PageList.create_pagelist(_page_num, _page_size, _total)

    # 获取所有server
    _rst = models.InfoServer.fetch_all(sn=_query_sn, orderby=_query_sort,
                                       offset=_offset, limit=_pagelist.pageSize)
    # 结果设置为pagelist的contents属性
    _pagelist.set_contents(_rst)
    # 响应页面
    return render_template('basicresources/infoserver.html', pageList=_pagelist,
                           query_sn=_query_sn, query_sort=_query_sort )


# 添加信息
@app.route('/infoserver/add', methods=['POST'])
@login_required
def addinfoserver():
    _infoserver = models.InfoServer.create_by_request(request)

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
            
    return json.dumps({'ok': ok, 'result': result})


# 更新信息
@app.route('/infoserver/update', methods=['POST'])
@login_required
def updateinfoserver():
    _infoserver = models.InfoServer.create_by_request(request)
       
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

    return json.dumps({'ok': ok, 'result': result})
