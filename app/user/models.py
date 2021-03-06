from app.ext import db


# 用户
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=False)


'''
id, showname, shownameen, director, leadingRole, type, country, language, duration, screeningmodel, openday, backgroundpicture, flag, isdelete
'''


# 电影
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    # 电影名
    showname = db.Column(db.String(64), index=True, nullable=False)
    #英文名
    shownameen = db.Column(db.String(256), index=True, nullable=False)
    #导演
    director = db.Column(db.String(256), index=True, nullable=False)
    #演员名
    leadingRole = db.Column(db.String(256), index=True, nullable=False)
    #类型
    type = db.Column(db.String(256), index=True)
    #地区
    country = db.Column(db.String(256), index=True)
    #语言
    language = db.Column(db.String(256), index=True)
    #片长
    duration = db.Column(db.Integer)
    #版本
    screeningmodel = db.Column(db.String(256))
    #上映时间
    openday = db.Column(db.DateTime)
    #海报
    backgroundpicture = db.Column(db.String(256))
    #标记
    flag = db.Column(db.Integer)
    #是否下架
    isdelete = db.Column(db.Boolean, default=False)


'''
name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag,isdelete
'''
#电影院
class Cinemas(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    #影院名
    name = db.Column(db.String(64), index=True, nullable=False)
    #城市
    city = db.Column(db.String(256))
    #区域
    district = db.Column(db.String(256))
    #影院地址
    address = db.Column(db.String(256))
    #联系电话
    phone = db.Column(db.String(256))
    #评分
    score = db.Column(db.Integer)
    #厅门
    hallnum = db.Column(db.Integer)
    #
    servicecharge = db.Column(db.String(256))
    astrict = db.Column(db.String(256))
    flag = db.Column(db.String(256))
    isdelete = db.Column(db.String(256))

#影厅
class Hall(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    #影院的外键
    cid = db.Column(db.Integer, db.ForeignKey('cinemas.cid'))
    # 厅名
    name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    # 座位
    seats = db.Column(db.String(256), default=0)
    is_delete = db.Column(db.Boolean, default=False)

#影院排期
class HallSchedule(db.Model):
    hsid = db.Column(db.Integer, primary_key=True)
    #原价
    or_price = db.Column(db.Numeric(10, 2))
    #折扣价
    dis_price = db.Column(db.Numeric(10, 2))
    # 开始时间
    start_time = db.Column(db.DateTime)
    #1未开始  2正在放映
    status = db.Column(db.Integer, default=False)
    is_delete = db.Column(db.Boolean, default=False)
    # 电影的外键
    mid = db.Column(db.Integer, db.ForeignKey('movies.id'))
    # 影厅的外键
    hid = db.Column(db.Integer, db.ForeignKey('hall.hid'))
    # 影院的外键
    cid = db.Column(db.Integer, db.ForeignKey('cinemas.cid'))

