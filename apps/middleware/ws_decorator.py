import traceback
from functools import wraps

from flask import request
from flask_socketio import disconnect, emit

from utils.jwt_instance import verify_jwt


def wsErrorHandler(func):
    @wraps(func)
    def inFunc(*args, **kwargs):
        try:
            token = request.args.get('token')
            if not token:
                emit('error', {'msg': '用户未登录，无法连接服务器，请重新登录'})
                disconnect()
                return
            user, result = verify_jwt(token.removeprefix('Bearer '))
            if not result:
                emit('error', {'msg': user})
                disconnect()
                return
            userID, username = user['userID'], user['username']
            return func(*args, **kwargs)
        except Exception as e:
            # # 获取详细的错误信息，包括行号
            # tb = traceback.extract_tb(e.__traceback__)
            # # 提取引发异常的最后一行的详细信息
            # filename, line, func_name, text = tb[-1]
            # filename = filename.split('\\')[-1].strip('.py')
            # error_message = str(e)
            # # 返回文件名、错误信息和行号
            # msg = f"文件 {filename} 的第 {line} 行 出现错误：{error_message}"
            # print(msg)
            if not func.__name__ == 'handle_disconnect':
                disconnect()
            raise e
    return inFunc
