import os

from dotenv import load_dotenv

load_dotenv()

JWT_EXPIRE_TIME = 12 * 60 * 60  # JWT 过期时间，单位为秒，默认30分钟
MSG_SINGLE_AMOUNT = 50  # 单次加载消息的数量
SECRET_KEY = os.environ.get('SECRET_KEY')
# 生产环境强烈建议从环境变量获取 SECRET_KEY，不要用默认值

# 数据库配置
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 推荐设置为 False，避免不必要的警告和开销
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# 同样，数据库URI应从环境变量或更安全的配置源获取

# Redis 配置
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_DB = int(os.environ.get('REDIS_DB'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')  # 密码可以为空字符串

# 应用通用设置
UPLOAD_FOLDER = '/static/avatars'
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 最大上传文件大小

# 日志级别 (通常在开发环境更详细)
DEBUG = os.environ.get('DEBUG') == 'TRUE'  # 是否开启调试模式
LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
