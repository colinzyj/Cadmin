# encoding:utf-8

import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

import gconf

LOGLEVEL = gconf.LOGLEVEL
LOGFILE = gconf.LOGFILE
BACKCNT = gconf.BACKCNT


def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        __logger = logging.getLogger(logger_name)
        __logger.setLevel(LOGLEVEL)

        # handler all
        filehandler = TimedRotatingFileHandler(LOGFILE, when='midnight', backupCount=BACKCNT)
        datefmt = "%Y-%m-%d %H:%M:%S"
        format_str = "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s"
        # formatter = logging.Formatter(format_str, datefmt)
        formatter = logging.Formatter(format_str)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(LOGLEVEL)
        __logger.addHandler(filehandler)

        __logger = logging.getLogger(logger_name)
    return __logger

logger = init_logger("cmdb")


if __name__ == '__main__':
    LOGLEVEL = logging.INFO
    LOGFILE = './xxx.log'
    logger = init_logger("cmdb")
    logger.error('request /user/login', exc_info=True)
    logger.error("test-error")
    logger.info("test-info")
    logger.warn("test-warn")
