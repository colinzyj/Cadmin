# encoding: utf-8
#系统模块
import json
# 第三方模块
from flask import render_template, request
# 导入自定义的app模块
from utils.pagelist import PageList
from usermanage.login_required import login_required
from usermanage.permit_required import permit_required
from usermanage.models.permitlist import Permit
from app import app


@app.route('/permit/list', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def permitlist():
    params = request.args if request.method == 'GET' else request.form
    _query_permitid = params.get('query_permitid', '')
    _query_permitname = params.get('query_permitname', '')
    _query_permitdesc = params.get('query_permitdesc', '')
    _page_size = params.get('pageSize', '')
    _page_num = params.get('pageNum', 1)
    _total = Permit.fetch_all(count=True, permit_id=_query_permitid, permit_name=_query_permitname, permit_desc=_query_permitdesc)

    # 生成pagelist对象
    _pagelist, _offset = PageList.create_pagelist(_page_num, _page_size, _total)
    # 获取所有用户
    _rst = Permit.fetch_all(permit_id=_query_permitid, permit_name=_query_permitname,
                            __permitdesc=_query_permitdesc, offset=_offset, limit=_pagelist.pageSize)
    # 结果设置为pagelist的contents属性
    _pagelist.set_contents(_rst)
    # 响应页面
    # print _pagelist
    return render_template('usermanage/permit.html', pageList=_pagelist, query_permitid=_query_permitid,
                           query_permitname=_query_permitname, query_permitdesc=_query_permitdesc)


@app.route('/permit/add', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def permitadd():
    _permit = Permit.create_by_request(request)

    # 检查用户提交的数据
    ok, result = _permit.validate_add()

    # 如果检查通过则添加到文件中
    if ok:
        if _permit.create():
            ok = True
            result = '添加成功'
        else:
            ok = False
            result = '添加失败'

    return json.dumps({'ok': ok, 'result': result})


# 更新信息
@app.route('/permit/update', methods=['POST'])
@login_required
@permit_required('20011')
def permitupdate():
    _permit = Permit.create_by_request(request)

    # 检查用户提交的数据
    ok, result = _permit.validate_modify()
    # 如果检查通过则添加到DB
    if ok:
        if _permit.update():
            ok = True
            result = '更新成功'
        else:
            ok = False
            result = '执行更新失败'

    return json.dumps({'ok': ok, 'result': result})


# 删除信息
@app.route('/permit/delete', methods=['POST'])
@login_required
@permit_required('20011')
def permitdelete():
    _permit = Permit.create_by_request(request)
    # print _permit.id
    ok, result = _permit.validate_delete()
    if ok:
        # 删除数据
        ok, result = _permit.delete(_permit.id)

    return json.dumps({'ok': ok, 'result': result})
