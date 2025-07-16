from apps.model.base_db import base_db
from apps.model.easy_model import EasyModel
from extensions import db


class ChatHistory(EasyModel, base_db):
    __tablename__ = 'chat_history'
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(1000))
    room_id = db.Column(db.Integer)
    role = db.Column(db.Integer, default=2)

    # 初始化
    def __init__(self, user_id=None, room_id=None, message=None, role=2):
        if room_id is not None:
            self.room_id = room_id
        if user_id is not None:
            self.user_id = user_id
        if message is not None:
            self.message = message
        self.role = role


class User(EasyModel, base_db):
    __tablename__ = 'user'
    account = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # sid = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    token = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.SmallInteger, default=0, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    status = db.Column(db.SmallInteger, default=1, nullable=False)  # 1正常2禁用
    is_delete = db.Column(db.SmallInteger, default=2, nullable=False)  # 2未删除1已删除

    # 初始化
    def __init__(self, account, password, username, avatar=None, token=None, is_admin=0, status=1, is_delete=2):
        self.account = account
        self.password = password
        self.username = username
        self.is_admin = is_admin
        self.token = token
        self.avatar = avatar
        self.status = status
        self.is_delete = is_delete


class Room(EasyModel, base_db):
    __tablename__ = 'room'
    name = db.Column(db.String(10), nullable=False)

    # 初始化
    def __init__(self, name):
        self.name = name
