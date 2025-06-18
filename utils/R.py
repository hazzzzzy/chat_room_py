

"""
    返回结果
    code 类型码 0-成功 1-失败
    data 数据
    msg 提示信息
    kwargs 其他参数
"""
from flask import jsonify


# 返回成功
def ok(data=None, msg="操作成功", code=0, **kwargs):
    result = {"code": code, "data": data, "msg": msg}
    if kwargs:
        result.update(kwargs)
    return jsonify(result)


# 返回失败
def failed(msg="操作成功", code=-1, **kwargs):
    result = {"code": code, "data": None, "msg": msg}
    if kwargs:
        result.update(kwargs)
    return jsonify(result)

