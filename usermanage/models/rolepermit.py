# encoding: utf-8

from utils.dbutil import execute_sql
from utils.loggerutil import logger

'''
DROP TABLE IF EXISTS `u_rolepermit`; 
 CREATE TABLE `u_rolepermit` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT '序号',
  `role_id` int(8) NOT NULL COMMENT '角色编号',
  `permit_id` int(8) NOT NULL COMMENT '权限编号，权限唯一标识',
  KEY `fk_permitid` (`permit_id`),
  KEY `fk_roleid` (`role_id`),
  CONSTRAINT `fk_roleid` FOREIGN KEY (`role_id`) REFERENCES `u_role` (`role_id`),
  CONSTRAINT `fk_permitid` FOREIGN KEY (`permit_id`) REFERENCES `u_permit` (`permit_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限对应关系'  
'''


class RolePermit(object):

    def __init__(self, roleid, permitid, rolename=[],permitname=[]):
        self.roleid=roleid
        self.rolename=rolename
        self.permitid=permitid
        self.permitname=permitname

    # 通过传入查询条件，模糊查询，返回role对象
    @classmethod
    def fetch_all(cls, **kwargs):
        _sql = 'select b.id,b.role_id,a.role_name,b.permit_id,c.permit_name from u_role a, u_rolepermit b, u_permit c  where a.role_id = b.role_id  and b.permit_id = c.permit_Id  '
        _params = []
        # print kwargs
        __roleid = kwargs.get('role_id', '')
        __permitid = kwargs.get('permit_id', '')
        # 处理查询条件,安全尽量不遍历kwargs做查询
        if __roleid != '':
            _sql += ' AND b.role_id in %s '
            _params.append(__roleid)
        if __permitid != '':
            _sql += ' AND b.permit_id in %s '
            _params.append(__permitid)

        _cnt, _rst = cls.execute(_sql, _params, True)
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

    @classmethod
    def execute(cls, sql, args=(), is_fetch=False):
        return execute_sql(sql, args, is_fetch)

# 测试的代码
if __name__ == '__main__':
    pass
