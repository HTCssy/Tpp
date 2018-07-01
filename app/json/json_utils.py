# import json
#
# from app.ext import db
# from app.home.models import Area
#
# keys = 'ABCDEFGHIJKLMNOPQRSJUVWXYZ'
# with open('area.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     obj = data.get('returnValue')
#     for key in keys:
#         cities = obj.get(key)
#         for city in cities:
#             db.session.add(Area(name=city.get('regionName'),
#                                 pingyin=city.get('pinYin'),
#                                 parent_id=city.get('parentId'),
#                                 area_id=city.get('cityCode'),
#                                 key=key,
#                                 ))
#             db.session.commit()
import datetime
from decimal import Decimal

from app.ext import db


def to_dict(object):
    obj = {}
    # 获取对象所有的字段
    keys = vars(object).keys()
    for key in keys:
        if not key.startswith('_'):
            #判断值是否是时间类型
            if isinstance(getattr(object, key), datetime.datetime):
                obj[key] = getattr(object, key).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(object, key), datetime.date):
                obj[key] = getattr(object, key).strftime('%Y-%m-%d')
            elif isinstance(getattr(object, key), Decimal):
                obj[key] = str(getattr(object, key))
            elif isinstance(getattr(object, key), db.Model):
                to_dict(getattr(object, key))
            elif isinstance(getattr(object, key), list):
                to_list(getattr(object, key))
            else:
                obj[key] = getattr(object, key)
    return obj


def to_list(objects):
    if isinstance(objects, list) and objects:
        objs = []
        for obj in objects:
            objs.append(to_dict(obj))
        return objs
