import json

import redis
from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message

from werkzeug.security import generate_password_hash,check_password_hash

from app.ext import db, mail, cache
from app.home.models import Area
from app.user.models import User

#配置缓存
HOST = '127.0.0.1'
PORT = 6379
DB = 0
# rds = redis.Redis()
pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB)
rds = redis.Redis(connection_pool=pool)

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login/')
def login():
    pass

'''
建表
    username
    password
    email
    is_active 1激活 0未激活 
'''
@user.route('/register/', methods=['POST', 'GET'])
def register():
    result = {}
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        email = request.values.get('email')
        if username and password and email:
            user = User.query.filter(User.username == username or User.email == email).all()
            if user:
                result.update(msg='账号或者邮箱已经存在', status = -2)
            else:
                pwd = generate_password_hash(password)
                user = User(username=username, password=pwd, email=email)
                db.session.add(user)
                db.session.commit()
            #发送激活邮箱
            msg = Message('激活邮件',
                          body='用户您好',
                          html=render_template('activate.html', username=username),
                          sender='13163318212@163.com',
                          recipients=[email])
            mail.send(msg)
            #将用户缓存到redis
            # rds.set('username', username, ex=10 * 60)
            cache.set('username', username, timeout=10*60)
        else:
            result.update(msg='必要参数不能为空', status=-1)
    else:
        result.update(msg='错误的请求方式', status=400)
    return jsonify(result)

# http://xxx/user/activate/?username=666
@user.route('/activate')
def activate_account():
    result = {}
    username = request.values.get('uname')
    if username == cache.get('username'):#rds.get('username')
        user = User.query.filter(User.username == username).first()
        if user:
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            result.update(status=200, msg='激活成功')
        else:
            result.update(status=-4, msg='激活用户不存在')
    else:
        result.update(status=-3, msg='激活链接失效,请重新激活')
    return jsonify(result)


@user.route('/add/')
def add_json_data():
    keys = 'ABCDEFGHIJKLMNOPQRSJUVWXYZ'
    with open(r'D:\xuexiziliao\third_Django\week_two\Tpp\app\json\area.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        obj = data.get('returnValue')
        for key in keys:
            cities = obj.get(key)
            for city in cities:
                db.session.add(Area(name=city.get('regionName'),
                                    pingyin=city.get('pinYin'),
                                    parent_id=city.get('parentId'),
                                    area_id=city.get('cityCode'),
                                    key=key,
                                    ))
                db.session.commit()
    return 'success'