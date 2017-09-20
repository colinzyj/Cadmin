#encoding: utf-8

from utils.dbutil import execute_sql

class MachineRoom(object):
    colums = ['uid', 'username', 'realname','password', 'telephone', 'status']
    sql_login = 'SELECT * FROM user WHERE username=%s AND password=md5(%s) AND status=0 LIMIT 1;'
    sql_fetch_all = 'SELECT %s FROM user where 1 '
    sql_get_by_keys = 'SELECT %s FROM user WHERE 1 '
    sql_insert = 'INSERT INTO user(username, realname, password, telephone, status) VALUES(%s, %s, md5(%s), %s, %s);'
    sql_update = 'UPDATE user SET %s WHERE uid=%%s;'
    sql_delete_by_key = 'DELETE FROM user WHERE uid=%s;'

    def get_machine_rooms(self):
        _sql = 'select machine_room_id,machine_room,status from machine_room'
        _cnt,_result = execute_sql(_sql,(),True)
        #print _result
        #print [zip(str(_value[0]), _value[1])) for _value in _result]
        #print [dict(zip(str(_value[0]), _value[1])) for _value in _result]
        #return [ dict(zip(str(_value[0]), _value[1])) for _value in _result]
        return _result


# 测试的代码
if __name__ == '__main__':
    pass
