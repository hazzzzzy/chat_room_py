from datetime import datetime


def model2dict(obj):
    if hasattr(obj, '__table__'):
        _ = {}
        for i in obj.__table__.columns:
            v = getattr(obj, i.name)
            if isinstance(v, datetime):
                _[i.name] = v.strftime('%Y-%m-%d %H:%M:%S')
            else:
                _[i.name] = v
        return _
        # return {c.name: getattr(obj, c.name) if isinstance(getattr(obj, c.name), datetime) for c in obj.__table__.columns}
    elif hasattr(obj, '_asdict'):
        return obj._asdict()
    elif isinstance(obj, tuple):
        # 自己写字段名
        raise ValueError("请自己写字段名")
    else:
        raise TypeError("不支持的类型")
