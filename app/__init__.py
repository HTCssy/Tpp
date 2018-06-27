from flask import Flask

from app.apis import register_blue
from app.config.setting import env
# from .config import setting
from app.ext import init_ext

app = Flask(__name__)
#创建app
def create_app(env_name):
    app.config.from_object(env.get(env_name))
    init_ext(app)
    register_blue(app)
    return app
