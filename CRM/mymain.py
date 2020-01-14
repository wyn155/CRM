from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


# 创建flask_sqlalchemy扩展
db = SQLAlchemy()
# 创建 restful apis
api = Api()

# 创建flask_login 扩展

def app_extend(app):
    # 连接 flask_sqlalchemy扩展
    db.init_app(app)
    api.init_app(app)
    return app