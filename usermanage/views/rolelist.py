# encoding: utf-8
# 系统模块
import json
# 第三方模块
from flask import render_template, request
# 导入自定义的app模块
from utils.pagelist import PageList
from usermanage.login_required import login_required
from usermanage.permit_required import permit_required
from usermanage.models.rolelist import Role
from app import app


@app.route('/role/list', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def rolelist():
    params = request.args if request.method == 'GET' else request.form
    _query_rolename = params.get('query_rolename', '')
    _query_roledesc = params.get('query_roledesc', '')
    _page_size = params.get('pageSize', '')
    _page_num = params.get('pageNum', 1)
    _total = Role.fetch_all(count=True, role_name=_query_rolename, role_desc=_query_roledesc)

    # 生成pagelist对象
    _pagelist, _offset = PageList.create_pagelist(_page_num, _page_size, _total)
    # 获取所有用户
    _rst = Role.fetch_all(role_name=_query_rolename, __roledesc=_query_roledesc, offset=_offset, limit=_pagelist.pageSize)
    # 结果设置为pagelist的contents属性
    _pagelist.set_contents(_rst)
    # 响应页面
    # print _pagelist
    return render_template('usermanage/role.html',pageList=_pagelist, query_rolename=_query_rolename,query_roledesc=_query_roledesc)


@app.route('/role/add', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def roleadd():
    _role = Role.create_by_request(request)
    # 检查用户提交的数据
    ok, result = _role.validate_add()

    # 如果检查通过则添加到文件中
    if ok:
        if _role.create():
            ok = True
            result = '添加成功'
        else:
            ok = False
            result = '添加失败'

    return json.dumps({'ok': ok, 'result': result})


# 更新信息
@app.route('/role/update', methods=['POST'])
@login_required
@permit_required('20011')
def roleupdate():
    _role = Role.create_by_request(request)

    # 检查用户提交的数据
    ok, result = _role.validate_modify()
    print ok,result
    # 如果检查通过则添加到DB
    if ok:
        if _role.update():
            ok = True
            result = '更新成功'
        else:
            ok = False
            result = '更新失败'

    return json.dumps({'ok': ok, 'result': result})


# 删除信息
@app.route('/role/delete', methods=['POST'])
@login_required
@permit_required('20011')
def roledelete():
    _role = Role.create_by_request(request)
    # print _role.id

    # 删除数据
    ok, result = _role.delete(_role.role_id)

    return json.dumps({'ok': ok, 'result': result})
