import traceback
from functools import wraps

from utils.R import failed


def errorHandler(func):
    @wraps(func)
    def inFunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 获取详细的错误信息，包括行号
            tb = traceback.extract_tb(e.__traceback__)
            # 提取引发异常的最后一行的详细信息
            filename, line, func_name, text = tb[-1]
            filename = filename.split('\\')[-1].strip('.py')
            error_message = str(e)
            # 返回文件名、错误信息和行号
            msg = f"文件 {filename} 的第 {line} 行 出现错误：{error_message}"
            return failed(msg)

    return inFunc
