# encoding: utf-8

from utils.dbbase import DBModel

'''
DROP TABLE IF EXISTS `info_server`;
CREATE TABLE `info_server` (
  `sn` VARCHAR(16) PRIMARY KEY NOT NULL COMMENT 'SN号,设备唯一标识',
  `assettag` VARCHAR(24) COMMENT '财务资产编号,作为资产的唯一标识',
  `brand` VARCHAR(24) COMMENT '品牌,IBM/DELL等',
  `model` VARCHAR(24) COMMENT '型号,R410,x3850等',
  `cpu` VARCHAR(64) COMMENT 'CPU信息和数量',
  `ram` VARCHAR(64) COMMENT '内存信息和数量',
  `disk` VARCHAR(64) COMMENT '硬盘信息和数量',
  `usize` TINYINT COMMENT '设备高度,多少U',
  `raidcard` VARCHAR(64) COMMENT 'Raid卡信息',
  `buytime` DATE COMMENT '购买时间',
  `guaranteetime` DATE COMMENT '保修过期时间',
  `note` TEXT COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 \
  COMMENT='服务器资产信息,记录SN对应资产配置,无使用信息,只新增,不删除';
'''


class InfoServer(DBModel):
    _table = 'info_server'
    _pk = 'sn'
    _columns = ['sn', 'assettag', 'brand', 'model', 'cpu', 'ram', 'disk', 'usize',
                'raidcard', 'buytime', 'guaranteetime', 'note']
    _columns_add = ['sn', 'assettag', 'brand', 'model', 'cpu', 'ram', 'disk', 'usize',
                    'raidcard', 'buytime', 'guaranteetime', 'note']
    _columns_update = ['cpu', 'ram', 'disk', 'raidcard', 'guaranteetime', 'note']

    # 通过传入条件，返回模糊匹配list
    @classmethod
    def fetch_all(cls, count=False, orderby='', offset=None, limit=None, **kwargs):
        _query = {}
        _query.setdefault('sql', '')
        _query.setdefault('args', [])
        __sn = kwargs.get('sn', '')
        __assettag = kwargs.get('assettag', '')

        # 处理查询条件，增加查询条件在这里添加，
        if __sn != '':
            _query['sql'] += ' AND sn LIKE %s '
            _query['args'].append('%' + __sn + '%')
        if __assettag != '':
            _query['sql'] += ' AND assettag LIKE %s '
            _query['args'].append('%' + __assettag + '%')

        # 如果是统计请求，根据条件返回条数
        if count:
            _cnt, _rst = cls.query_count(query=_query)
            return _rst[0][0] if _cnt > 0 else 0

        _cnt, _rst = cls.query_all(orderby=orderby, offset=offset, limit=limit, query=_query)
        return _rst

    def validate_add(self):
        return True, '校验成功'

    def validate_modify(self):
        return True, '校验成功'


# 测试的代码
if __name__ == '__main__':
    pass
