# encoding: utf-8

import MySQLdb

import gconf
from utils.loggerutil import logger

'''
数据库操作步骤
1. 创建数据库连接
2. 获取游标
3. 执行sql语句
4. 提交事物(增删改)或获取查询结果(查)
5. 关闭游标
6. 关闭数据库连接
'''


# @method 执行sql
# @param str sql 需要执行的sql语句
# @param tuple args 预定义的变量，默认为空元组
# @param boolean is_fetch 是否为查询语句，默认为False 
def execute_sql(sql, args=(), is_fetch=False):
    _conn, _cur = None, None
    _rt_cnt, _rt_fetch = 0, ()

    try:
        # 步骤1
        _conn = MySQLdb.connect(host=gconf.DB_HOST, port=gconf.DB_PORT,
                                user=gconf.DB_USER, passwd=gconf.DB_PASSWD,
                                db=gconf.DB_NAME, charset=gconf.DB_CHARSET)

        _cur = _conn.cursor()    # 步骤2
        # print sql,args
        _rt_cnt = _cur.execute(sql, args)                   # 步骤3
        logger.info('excute %s,%s' % (sql, args))
        if is_fetch:                                        # 步骤4  判断是否为查询还是修改动作
            _rt_fetch = _cur.fetchall()                         # 查询操作
        else:
            _conn.commit()
    except BaseException, e:
        pass
        logger.error('sql excute error %s', str(e), exc_info=True)
    finally:
        if _cur is not None:
            _cur.close()                                    # 步骤5
        if _conn is not None:
            _conn.close()                                   # 步骤6

    return _rt_cnt, _rt_fetch                               # 返回结果

if __name__ == '__main__':
    _cnt, _rs = execute_sql(sql='select b.id,b.role_id,a.role_name,c.permit_id,c.permit_name from u_role a, u_rolepermit b, u_permit c  where a.role_id = b.role_id    and b.permit_id = c.permit_Id  order by a.role_Id;', is_fetch=True)
    print _cnt
    print _rs