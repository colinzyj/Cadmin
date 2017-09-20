# encoding: utf-8
# 系统模块
import json
# 第三方模块
from flask import request
# 导入自定义的app模块
from usermanage.login_required import login_required
from usermanage.permit_required import permit_required
from usermanage.models.rolepermit import RolePermit
from app import app


@app.route('/rolepermit/listbyrid', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def rolepermitlistbyrid():
    params = request.args if request.method == 'GET' else request.form
    _query_roleid = params.getlist('roleid')
    print _query_roleid
    # 获取所有结果
    _rst = RolePermit.fetch_all(role_id=_query_roleid)
    # 筛选结果，只返回需要数据
    _rst = [list([x[3], x[4]]) for x in _rst]

    return json.dumps({'result': _rst})


@app.route('/rolepermit/listbypid', methods=['GET', 'POST'])
@login_required
@permit_required('20011')
def rolepermitlistbypid():
    params = request.args if request.method == 'GET' else request.form
    _query_permitid = params.getlist('permitid')
    print _query_permitid
    # 获取所有结果
    _rst = RolePermit.fetch_all(permit_id=_query_permitid)
    # 筛选结果，只返回需要数据
    _rst = [list([x[1], x[2]]) for x in _rst]

    return json.dumps({'result': _rst})


@app.route('/rolepermit/unbind', methods=['POST'])
@login_required
@permit_required('20011')
def rolepermitunbind():
    params = request.args if request.method == 'GET' else request.form
    #_query_permitid = params.getlist('permitid[]')
    _query_permitid1 = params.get('permitid')
    _query_permitid = list(set(_query_permitid1.split(',')))
    _query_roleid = params.getlist('roleid')
    print _query_permitid
    print _query_roleid
    print _query_permitid1
    # 获取所有结果
    #_rst = RolePermit.unbindpermit(permit_id=_query_permitid, role_id=_query_roleid)
    # 筛选结果，只返回需要数据
    #_rst = [list([x[1], x[2]]) for x in _rst]

    return json.dumps({'ok':True, 'result': '操作完成'})