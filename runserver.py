# encoding:utf-8
from app import app

if __name__ == '__main__':
    # app.logger.error('server start on 8000')
    app.run(host='0.0.0.0', port=8000, debug=True)
    pass
