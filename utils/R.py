"""
    返回结果
    code 类型码 0-成功 1-失败
    data 数据
    msg 提示信息
    kwargs 其他参数
"""
import json

from flask import jsonify, Response


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


def agnoStreamOk(agentResponse):
    def generate():
        for event in agentResponse:
            if event.event == "RunContent":
                chunk = {
                    "v": event.content
                }
                # 注意 SSE 格式：必须是 "data: ..."，然后两个换行
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        yield 'event: finish\ndata:{}\n\n'

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            'Content-Type': 'text/event-stream',
        }
    )
