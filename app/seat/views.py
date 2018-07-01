from flask import Blueprint, request, jsonify

from app.json.json_utils import to_dict
from app.seat.models import Seat, SeatSchedule
from app.user.models import HallSchedule, Cinemas, Hall, Movies

seat_bule = Blueprint('seat_bule', __name__)



# 选座
"""
必要参数:排片ID
必要参数 影片的id
必传参数 影院的id
"""
@seat_bule.route('/choose/')
def choose_seat():
    result = {}
    try:
        hsid = request.values.get('hsid', type=int)
        cid = request.values.get('cid', type=int)
        mid = request.values.get('mid', type=int)
        #查询排片的数据
        hs = HallSchedule.query.get(hsid)
        #查询影院的相关信息
        cinemas = Cinemas.query.with_entities(Cinemas.cid, Cinemas.name).filter(Cinemas.cid == cid).first()
        cinema = {}
        #过滤字段转化成字典
        cinema.update(cid=cinemas[0], name=cinemas[1])
        #查询影厅的相关信息
        halls = Hall.query.with_entities(Hall.name).filter(Hall.hid == hs.hid).first()
        #查询电影
        movies = Movies.query.with_entities(Movies.language, Movies.showname, Movies.screeningmodel,
                                           Movies.backgroundpicture).filter(Movies.id == hs.mid).first()
        # 通过影院id 影厅的id 去查询相关的座位信息
        seat_list = SeatSchedule.query.filter(SeatSchedule.cinema_id == 1, SeatSchedule.hall_id == 1).all()
        # 第一个就是x y status
        result.update(status=200, msg='success', cinema=cinema, hall_schedule=to_dict(hs))
    except:
        result.update(status=404, msg='请求失败')
    return jsonify(result)




