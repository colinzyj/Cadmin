# encoding:utf-8
from flask import Flask

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX aHH!sajmN]LWX/,?RT'

# import views
from website import index
# from usermanage.views import permitlist , rolelist, rolepermit, user
from usermanage2.views import permitlist