from app.ext import db


class Area(db.Model):
    area_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    #省份
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    #关联的市县或区
    parent_id = db.Column(db.Integer, index=True)
    #拼音
    pingyin = db.Column(db.String(100), nullable=False, index=True)
    #A-Z开头
    key = db.Column(db.String(10))
    #热门城市
    is_hot = db.Column(db.Boolean, default=False)


class Banner(db.Model):
    banner_id = db.Column(db.Integer, primary_key=True)
    #图片地址
    img_url = db.Column(db.String(10))
    is_delete = db.Column(db.Boolean, default=False)