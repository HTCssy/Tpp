from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



def init_ext(app):
    init_db(app)
    init_mail(app)
    init_cache(app)
    init_cors(app)

#配置数据库迁移
db = SQLAlchemy()
#数据库迁移
migrate = Migrate()

#初始化数据配置
def init_db(app):
    db.init_app(app=app)
    migrate.init_app(app, db)


#后台admin配置
# admin = Admin(app)
# def init_admin(app):
#     pass

#邮箱的配置
mail = Mail()
def init_mail(app):
    mail.init_app(app)


#缓存配置
"""
安装
1> flask-caching
2> redis
配置
"""
cache = Cache()
def init_cache(app):
    cache.init_app(app,
                   config={'CACHE_TYPE': 'redis'}
                    )


#跨域请求问题配置
cors = CORS()
def init_cors(app):
    cors.init_app(app, supports_credentials=True)