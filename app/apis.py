from flask import Blueprint, Flask


#蓝图注册
from app.home.views import home
from app.seat.views import seat_bule
from app.user.views import user


def register_blue(app:Flask):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(home)
    app.register_blueprint(seat_bule)