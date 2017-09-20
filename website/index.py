# encoding: utf-8
import sys

from flask import redirect  # 重定向到其他url
from flask import render_template  # 加载模板
from flask import session

from utils.loggerutil import logger
# 引入flask中的必要类和函数
# from app import app

reload(sys)
sys.setdefaultencoding('utf-8')

from app import app

# homepage
# 定义路由, 如果以GET方式访问url地址为/则由index函数处理
@app.route('/')
def index():
    logger.info('request /')
    if session.get('user') is not None:
        __username = session.get('user')
        logger.warning('%s request / with valid session' % __username)
        return redirect('/user/list')
    # 返回templates目录下的login.html模板中的内容
    return redirect('/user/login')

