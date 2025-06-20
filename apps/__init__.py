import eventlet
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from apps.views import register_blueprint
from apps.ws import register_ws
from extensions import db

eventlet.monkey_patch()
socketio = SocketIO(
    cors_allowed_origins='*',
    engineio_logger=False,
    logger=False,
    ping_timeout=10,
    ping_interval=5,
    async_mode='eventlet')


def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        'cRoom', '4tP2priPEsiEfABR', '119.45.219.7', 3306, 'croom')
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    register_blueprint(app)

    # 注册WebSocket事件处理程序
    register_ws(app, socketio)

    # 将socketio与app关联
    socketio.init_app(app)

    return app
