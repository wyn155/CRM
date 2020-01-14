from flask import Flask
from mymain import app_extend,db
from api import register_api
from myblueprints.search_blueprints import search
# 导入表，解决无法创建表的问题
import model



# 创建flask应用
def create_app():
    app = Flask(__name__)
    app.register_blueprint(search)
    app.config.from_object("config")
    register_api()
    # 连接所有扩展
    app_extend(app)
    with app.app_context():
        db.create_all()

    return app
