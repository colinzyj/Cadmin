# encoding: utf-8

from utils.dbbase import DBModel
#from utils.loggerutil import logger

'''
DROP TABLE IF EXISTS `u_permit`;
CREATE TABLE `u_permit` (
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT COMMENT '序号',
  `permit_id` INT(8) UNIQUE NOT NULL COMMENT '权限编号，权限唯一标识',
  `permit_name` VARCHAR(32) NOT NULL COMMENT '权限名称',
  `permit_desc` VARCHAR(64) COMMENT '权限描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 \
  COMMENT='所有权限值列表';
'''


class Permit(DBModel):
    _table = 'u_permit'
    _pk = 'id'
    _columns = ['id', 'permit_id', 'permit_name', 'permit_desc']
    _columns_add = ['permit_id', 'permit_name', 'permit_desc']
    _columns_update = _columns

    # @classmethod
    # def create_by_request(cls, req):
    #     _kwargs = {}
    #     for _column in cls._columns:
    #         _kwargs[_column] = req.form.get(_column, req.args.get(_column, cls._defaults.get(_column, '')))
    #     _kwargs['id']=req.form.getlist('id')
    #     print _kwargs
    #     return cls.create_object(**_kwargs)
    #
    # @classmethod
    # def create_object(cls, **kwargs):
    #     # pass
    #     _obj = cls()
    #     for _key, _value in kwargs.items():
    #         setattr(_obj, _key, _value)
    #     return _obj

    # 通过传入查询条件，模糊查询，返回Permit对象
    @classmethod
    def fetch_all(cls, count=False, offset=None, limit=None, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])
        # print kwargs
        __permitname = kwargs.get('permit_name', '')
        __permitid = kwargs.get('permit_id', '')
        __permitdesc = kwargs.get('permit_desc', '')
        # print kwargs
        # print __permitid != ''
        # 处理查询条件,安全尽量不遍历kwargs做查询
        if __permitid != '':
            _query['sql'] += ' AND permit_id like %s '
            _query['args'].append('%' + __permitid + '%')
        if __permitname != '':
            _query['sql'] += ' AND permit_name like %s '
            _query['args'].append('%' + __permitname + '%')
        if __permitdesc != '':
            _query['sql'] += ' AND permit_desc like %s '
            _query['args'].append('%' + __permitdesc + '%')

        # 如果是统计请求，返回查询条数
        if count:
            _cnt, _rst = cls.query_count(query=_query)
            return _rst[0][0] if _cnt > 0 else 0

        _cnt, _rst = cls.query_all(offset=offset, limit=limit, query=_query)
        return _rst

    # 通过传入条件，返回一个Permit对象
    @classmethod
    def get_by_keys(cls, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])

        if kwargs.get('permit_id') is not None:
            _query['sql'] += ' AND permit_id=%s '
            _query['args'].append(kwargs.get('permit_id'))

        _cnt, _rst = cls.query_all(query=_query)
        return _rst if _cnt > 0 else None

    # 验证信息合法性
    def validate_add(self):
        if self.permit_id == '' or self.permit_name == '':
            return False, 'ID和名称不能为空'
        if not str(self.permit_id).isdigit() or len(self.permit_id) != 5:
            return False, 'ID必须是长度为5的数字'

        _permit = self.get_by_keys(permit_id=self.permit_id)
        print _permit
        if _permit is not None:
            return False, '该权限值已经存在'

        return True, ''

    def validate_modify(self):
        if self.permit_id == '' or self.permit_name == '':
            return False, 'ID和名称不能为空'
        if not str(self.permit_id).isdigit() or len(self.permit_id) != 5:
            return False, 'ID必须是长度为5的数字'

        return True, ''

    def validate_delete(self):
        return True, ''
        # return False, '现在不给删'

# 测试的代码
if __name__ == '__main__':
    pass
