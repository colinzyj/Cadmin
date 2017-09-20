# encoding: utf-8

from utils.dbbase import DBModel
from utils.loggerutil import logger

'''
DROP TABLE IF EXISTS `user`;  
 CREATE TABLE `user` (
  `uid` INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` VARCHAR(16) UNIQUE NOT NULL COMMENT '登陆账户',
  `realname` VARCHAR(16) NOT NULL COMMENT '真实姓名',
  `password` VARCHAR(32) NOT NULL COMMENT '密码',
  `telephone` VARCHAR(16) NOT NULL COMMENT '电话号码',
  `status` INT(11) DEFAULT '1'  COMMENT '0可用,1仅新增不可登陆,2禁用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


class User(DBModel):
    _table = 'user'
    _pk = 'uid'
    _columns = ['uid', 'username', 'realname', 'password', 'telephone', 'status']
    _columns_add = ['username', 'realname', 'password', 'telephone', 'status']
    _defaults = {'status': 1}

    def login(self):
        _query = {}
        _query['sql'] = ' AND username=%s AND password=md5(%s) AND status=0 '
        _query['args'] = [self.username, self.password]
        logger.info('user: %s login', self.username)
        _cnt, _ = self.query_all(query=_query)
        print _cnt > 0,_query
        return _cnt > 0

    # 通过传入查询条件，模糊查询，返回User对象
    @classmethod
    def fetch_all(cls, count=False, offset=None, limit=None, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])
        __status = kwargs.get('status', '')
        __username = kwargs.get('username', '')
        
        # 处理查询条件
        if __username != '':
            _query['sql'] += ' AND username like %s '
            _query['args'].append('%' + __username + '%')
        if len(__status) != 0:
            _query['sql'] += ' AND status in %s '
            _query['args'].append(__status)

        # 如果是统计请求，返回查询条数
        if count:
            _cnt, _rst = cls.query_count(query=_query)
            return _rst[0][0] if _cnt > 0 else 0

        _cnt, _rst = cls.query_all(offset=offset, limit=limit, query=_query)
        return _rst

    # 通过传入条件，返回一个User对象
    @classmethod
    def get_by_keys(cls, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])

        if kwargs.get('uid') is not None:
            _query['sql'] += ' AND uid=%s '
            _query['args'].append(kwargs.get('uid'))

        if kwargs.get('username') is not None:
            _query['sql'] += ' AND username=%s '
            _query['args'].append(kwargs.get('username'))

        _cnt, _rst = cls.query_all(query=_query)
        return _rst if _cnt > 0 else None

    # 验证新增用户信息合法性
    def validate_add(self):
        if self.username == '' or self.password == '':
            return False, '用户名或密码不能为空'
        if not str(self.telephone).isdigit() or len(self.telephone) != 11 or not str(self.telephone).startswith('1'):
            return False, '手机号码不正确'
        
        _user = self.get_by_keys(username=self.username)
        if _user is not None:
            return False, '用户已注册'
        
        return True, ''

    # 验证修改用户信息合法性
    def validate_modify(self):
        if not str(self.telephone).isdigit() or len(self.telephone) != 11 or not str(self.telephone).startswith('1'):
            return False, '手机号码不正确'
            
        return True, ''

    def update(self):
        if self.password != '':
            self._columns_update = ['realname', 'password', 'telephone', 'status']
        else:
            self._columns_update = ['realname', 'telephone', 'status']
        # 定义新增列项后调用父函数update方法
        return super(User, self).update()


# 测试的代码
if __name__ == '__main__':
    pass
