import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import func, distinct, or_

from app.ext import db
from app.home.models import Area, Banner
from app.home.schema import movies_schmae, cinemas_schmae
from app.json.json_utils import to_list
from app.user.models import Movies, Cinemas, HallSchedule

#注册app
home = Blueprint('home', __name__)

#地址
keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
@home.route('/areas/')
def get_ares():
    result = {}
    ares = {}
    try:
        for key in keys:
            # with_entities 过滤列
            # 相当于 db.session
            # ares[key] = Area.query.with_entities(Area.name, Area.area_id).filter(Area.key == key).all()
            area_list = Area.query.filter(Area.key == key).all()
            if area_list is not None:
                ares[key] = to_list(area_list)
            result.update(msg='success', status=200, ares=ares)
    except:
        result.update(msg='查询失败', status=404)
    return jsonify(result)

#轮播图
@home.route('/img_url/', methods=['POST', 'GET'])
def img_url():
    result = {}
    try:
        img_url = Banner.query.with_entities(Banner.img_url).all()
        if img_url:
            result.update(status=200, msg='success', img_url=img_url)
        else:
            result.update(status=-1, msg='参数不存在')
    except:
        result.update(status=404, msg='fail')
    return jsonify(result)



@home.route('/movies/', methods=['POST', 'GET'])
def movies():
    result = {}
    try:
        movie = {}
        #分组统计次数
        counts = Movies.query.with_entities(Movies.flag, func.count("*")).group_by(Movies.flag).all()
        #正在热映
        hot_mov = Movies.query.filter(Movies.flag == 1).limit(5).all()
        #即将上映
        fut_mov = Movies.query.filter(Movies.flag == 2).limit(5).all()
        movie.update(counts=counts, hot_mov=to_list(hot_mov), fut_mov=to_list(fut_mov))
        result.update(status=200, msg='success', data=movie)
    except:
        result.update(status=404, msg='fail')
    return jsonify(result)



"""
参数flag
参数page
参数size

"""
#全部影片
# movies/?flag=1
@home.route('/movies_all/', methods=['POST', 'GET'])
def movies_all():
    result = {}
    try:
        #判断是热门还是即将上映
        flag = request.values.get('flag', default=1, type=int)
        #分页参数
        page = request.values.get('page', default=1, type=int)
        #每页显示的条数
        size = request.values.get('size', default=10, type=int)
        #分页查询数据
        paginate = Movies.query.filter(Movies.flag == flag).paginate(page=page, per_page=size, error_out=False)
        # movies = Movies.query.filter(Movies.flag == flag)
        """
        total 总条数
        pages 总页数
        items 数据
        """
        #封装前端界面所需的数据
        pagination = {'total': paginate.total,
                      'pages': paginate.pages}
        # 将对象转为字典,要显示的主要数据
        movies = movies_schmae.dump(paginate.items)
        #组装返回的数据
        result.update(status=200, msg='success', data=movies.data, paginate=pagination)
    except Exception as e:
        result.update(status=404, msg='fail')
    return jsonify(result)



#影院
@home.route('/cinemas/', methods=['POST', 'GET'])
def cinemas():
    result = {}
    try:
        # 分页参数
        page = request.values.get('page', default=1, type=int)
        #每页的条数
        size = request.values.get('size', default=10, type=int)
        #城市
        city = request.values.get('city')
        #城市的区县
        dist = request.values.get('dist')
        #搜索电影院的名称
        keyword = request.values.get('keyword')
        #sort 1按评分降序  2表示评分升序 0表示综合排序
        sort = request.values.get('sort', default=0)
        if city:
            #根据城市分页加载数据
            query = Cinemas.query.filter(Cinemas.city == city)
            #如果选择了区县
            if dist:
                query = query.filter(Cinemas.district == dist)
            if keyword:
                #根据关键字电影院名查询
                query = query.filter(Cinemas.name.like('%' + keyword + '%'))
            if sort:
                #升序
                if sort == 1:
                    query =query.order_by(Cinemas.score)
                else:
                    #降序
                    query = query.order_by(Cinemas.score.desc())
            #前端的数据
            paginate = query.paginate(page=page, per_page=size, error_out=False)
            #将对象转为字典 to_list自定义方法
            movies = to_list(paginate.items)
            #添加到字典
            result.update(status=200, msg='success', cinemas=movies)
        else:
            result.update(status=-1, msg='参数不存在')
    except:
        result.update(status=404, msg='fail')
        #返回json数据
    return jsonify(result)


#电影详情和放映
#必要参数城市  和 电影的id
@home.route('/detail/', methods=['POST', 'GET'])
def show_detail():
    result = {}
    try:
        #获取电影的id
        mid = request.values.get('mid')
        #获取所选的城市
        city = request.values.get('city')
        #通过城市获得地区
        dist = request.values.get('dist')
        #获取影院id
        cid = request.values.get('cid', default=0, type=int)
        if mid and city:
            #获取影片详细信息
            movie = db.session.query(Movies.id, Movies.backgroundpicture, Movies.director, Movies.leadingRole, Movies.country, Movies.language).filter(Movies.id == mid).first()
            # 通过城市查询地区的相关的信息
            #  distinct去重
            # with_entities 过滤列 返回元组
            districts = Cinemas.query.with_entities(distinct(Cinemas.district)).filter(Cinemas.city == city).all()
            #通过城市查询影院的相关信息
            query = Cinemas.query.order_by(Cinemas.cid).filter(Cinemas.city == city)
            #判断是否请求区县数据
            if dist:
                query = query.filter(Cinemas.district == dist)
            cinemas = query.all()
            # 如果前端点击了影院使用选中影院
            cid = cid if cid else cinemas[0].cid
            # 通过电影的id和影院的id 就能查出所有的当前影院该影片的拍档情况
            hall_schedules = HallSchedule.query.filter(HallSchedule.cid == cid).filter(HallSchedule.mid == mid).filter(or_(HallSchedule.start_time >= datetime.datetime.now()),HallSchedule.start_time < start_time()).all()
            result.update(status=200,
                          msg='success',
                          districts=districts,
                          cinemas=to_list(cinemas),
                          hall_schedules=to_list(hall_schedules),
                          movie=movie)
    except Exception as e:
        result.update(status=404, msg='error')
    return jsonify(result)


#开始放映时间
def start_time():
    #现在时间
    now = datetime.datetime.now()
    #今天零点
    today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    #最后放映时间
    last = today + datetime.timedelta(hours=23, minutes=59, seconds=59)
    return last
