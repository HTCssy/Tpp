

#座位表
import datetime

from app.ext import db
from app.user.models import Cinemas, Hall, HallSchedule


class Seat(db.Model):
    __tablename__ = "seat"
    seat_id = db.Column(db.Integer, primary_key=True)
    # 1 普通,2 沙发 3 豪华包间
    # type = db.Column(db.Integer, default=1)
    #座位的x
    seat_x = db.Column(db.Integer)
    #座位的Y  通过x ,y 能确定一个座位
    seat_y = db.Column(db.Integer)
    # 1表示可用  2 表示损坏
    status = db.Column(db.Integer, default=1)
    #是否删除 1表示正常 0表示删除  表的公共字段
    is_delete = db.Column(db.Integer, default=1)
    # 记录创建时间 表的公共字段
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    ##  ====关联字段=====
    # 影院的id
    cinema_id = db.Column(db.Integer, db.ForeignKey(Cinemas.cid))
    # 影厅的id
    hall_id = db.Column(db.Integer, db.ForeignKey(Hall.hid))

#座位排期表
class SeatSchedule(db.Model):
    ssid = db.Column(db.Integer, primary_key=True)
    #关联座位id
    seat_id = db.Column(db.Integer, db.ForeignKey(Seat.seat_id))
    # 影院的id
    cinema_id = db.Column(db.Integer, db.ForeignKey(Cinemas.cid))
    # 影厅的id
    hall_id = db.Column(db.Integer, db.ForeignKey(Hall.hid))
    # 关联排档的id
    hsid = db.Column(db.Integer, db.ForeignKey(HallSchedule.hsid))
    # 1表示未锁定   2 表示锁定未支付   3表示锁定已支付
    status = db.Column(db.Integer, default=1)
    # 是否删除 1表示正常   0表示 记录被删除  表的公共字段
    is_delete = db.Column(db.Integer, default=1)
    # 该记录创建的时间  表的公共字段
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    seat = db.relationship('Seat')