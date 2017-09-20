# encoding: utf-8

from utils.dbbase import DBModel
#from utils.loggerutil import logger

'''
DROP TABLE IF EXISTS `u_role`;
CREATE TABLE `u_role` (
  `role_id` INT(8) PRIMARY KEY AUTO_INCREMENT COMMENT '角色编号',
  `role_name` VARCHAR(16) NOT NULL COMMENT '角色名称',
  `role_desc` VARCHAR(64) COMMENT '角色描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 \
  COMMENT='所有角色列表';
'''


class Role(DBModel):
    _table = 'u_role'
    _pk = 'role_id'
    _columns = ['role_id', 'role_name', 'role_desc']
    _columns_add = ['role_name', 'role_desc']
    _columns_update = _columns

    # 通过传入查询条件，模糊查询，返回role对象
    @classmethod
    def fetch_all(cls, count=False, offset=None, limit=None, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])
        # print kwargs
        __rolename = kwargs.get('role_name', '')
        __roledesc = kwargs.get('role_desc', '')
        # print kwargs
        # print __roleid != ''
        # 处理查询条件,安全尽量不遍历kwargs做查询
        if __rolename != '':
            _query['sql'] += ' AND role_name like %s '
            _query['args'].append('%' + __rolename + '%')
        if __roledesc != '':
            _query['sql'] += ' AND role_desc like %s '
            _query['args'].append('%' + __roledesc + '%')

        # 如果是统计请求，返回查询条数
        if count:
            _cnt, _rst = cls.query_count(query=_query)
            return _rst[0][0] if _cnt > 0 else 0

        _cnt, _rst = cls.query_all(offset=offset, limit=limit, query=_query)
        return _rst

    # 通过传入条件，返回一个role对象
    @classmethod
    def get_by_keys(cls, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])

        if kwargs.get('role_name') is not None:
            _query['sql'] += ' AND role_name=%s '
            _query['args'].append(kwargs.get('role_name'))

        _cnt, _rst = cls.query_all(query=_query)
        return _rst if _cnt > 0 else None

    # 验证信息合法性
    def validate_add(self):
        if self.role_name == '':
            return False, '角色名称不能为空'
        _role = self.get_by_keys(role_name=self.role_name)
        # print _role
        if _role is not None:
            return False, '该角色已经存在'
        return True, ''

    def validate_modify(self):
        if self.role_name == '':
            return False, '角色名称不能为空'
        return True, ''


# 测试的代码
if __name__ == '__main__':
    pass
