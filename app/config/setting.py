import uuid

uuid.uuid1()
class Config():
    DEBUG = False
    SECRET_KEY = uuid.uuid1()


def get_db_uri(database:dict):
    user = database.get('USER') or 'root'
    password = database.get('PASSWORD') or '123456'
    host = database.get('HOST') or '127.0.0.1'
    port = database.get('PORT') or '3306'
    name = database.get('NAME') or 'TTP'
    db = database.get('DB') or 'mysql'
    driver = database.get('DRIVER') or 'pymysql'
    charset = database.get('CHARSET') or 'utf8'
    return "{}+{}://{}:{}@{}:{}/{}?charset={}".format(db,driver,user,password,host,port,name,charset)


#开发
class DevelopConfig(Config):
    DEBUG = True
    DATABASES = {
        'DB': 'mysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'TPP',
        'DRIVER': 'pymysql',
        'CHARSET': 'utf8',
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASES)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #发送邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = '13163318212@163.com'
    MAIL_PASSWORD = 'woaini520'


#生产
class ProductConfig(Config):
    DEBUG = False
    DATABASE = {
        'DB': 'mysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'TPP',
        'DRIVER': 'pymysql',
        'CHARSET': 'utf8',
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


env = {
    #开发环境
    'dev':DevelopConfig,
    #生产环境
    'pro':ProductConfig,
}