import traceback
from functools import wraps

from flask import request

from utils import R
from utils.jwt_instance import verify_jwt

ignoreList = ['/login']
ignoreList = [f'/api{path}' for path in ignoreList]  # 添加前缀以匹配完整路径


def errorHandler(func):
    @wraps(func)
    def inFunc(*args, **kwargs):
        try:
            if request.path not in ignoreList:
                token = request.headers.get('Authorization')
                if not token:
                    return R.failed(code=-2, msg='用户未登录，请重新登录')
                token = token.removeprefix('Bearer ')
                user, result = verify_jwt(token)
                if not result:
                    return R.failed(code=-2, msg='登录已过期，请重新登录')
                userID = user['userID']
                username = user['username']
                return func(*args, userID=userID, username=username, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            # 获取详细的错误信息，包括行号
            tb = traceback.extract_tb(e.__traceback__)
            # 提取引发异常的最后一行的详细信息
            filename, line, func_name, text = tb[-1]
            filename = filename.split('\\')[-1].strip('.py')
            error_message = str(e)
            if e.__dict__.get('_digest_msg'):
                error_message = '存储桶操作失败：' + e.__dict__.get('_digest_msg').get('message') or e
            # 返回文件名、错误信息和行号
            msg = f"文件 {filename} 的第 {line} 行 出现错误：{error_message}"
            print(msg)
            return R.failed('服务器错误，请联系管理员')

    return inFunc
