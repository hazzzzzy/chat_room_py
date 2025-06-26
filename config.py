import os

from dotenv import load_dotenv

load_dotenv()


# 定义基础配置类
class Config:
    """
    基础配置类，包含所有环境共享的默认配置。
    """
    JWT_EXPIRE_TIME = 12 * 60 * 60  # JWT 过期时间，单位为秒，默认30分钟
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
    UPLOAD_FOLDER = '/path/to/upload/folder'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小

    # 日志级别 (通常在开发环境更详细)
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'


class DevelopmentConfig(Config):
    """
    开发环境配置类，继承基础配置并覆盖或添加开发特有项。
    """
    DEBUG = True  # 开启 Flask 的调试模式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cRoom:4tP2priPEsiEfABR@119.45.219.7:3306/croom'
    # 开发环境的 Redis 可以指向本地
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

class ProductionConfig(Config):
    """
    生产环境配置类，继承基础配置并覆盖或添加生产特有项。
    """
    DEBUG = False  # 生产环境绝不能开启 DEBUG
    TESTING = False
    ENV = 'production'
    # 生产数据库 URI 必须从环境变量获取，不能有默认值
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # 生产 Redis 必须从环境变量获取，不能有默认值
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')  # 生产环境密码不能为空
    # 生产日志只记录重要信息
    LOG_LEVEL = 'INFO'
    # 其他生产特有设置
    SESSION_COOKIE_SECURE = True  # 确保 Cookie 只通过 HTTPS 发送
    SESSION_COOKIE_HTTPONLY = True  # 防止客户端脚本访问 Cookie
    REMEMBER_COOKIE_SECURE = True
    # 对于 SocketIO
    # if using RabbitMQ or Kafka for message queue, configure it here
    # SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE_URL')
