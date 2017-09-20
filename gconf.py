# encoding: utf-8

import logging

# 数据库配置
DB_HOST = '172.18.0.73'
DB_PORT = 3306
DB_USER = 'cmdbuser'
DB_PASSWD = 'Lkc7e1jcw2.dal'
DB_NAME = 'CMDB'
DB_CHARSET = 'utf8'

# 默认分页大小
PAGESIZE = 10

# log配置
LOGLEVEL = logging.INFO    # 可选值 logging.xxx  xxx in (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOGFILE = 'logs/cmdb.log'  # 日志文件路径
BACKCNT = 30                # 归档日志数量