from apps.model.EasyModel import EasyModel
from apps.model.base_db import base_db
from extensions import db


class ChatHistory(EasyModel, base_db):
    __tablename__ = 'chat_history'
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(1000))
    room_id = db.Column(db.Integer)

    # 初始化
    def __init__(self, user_id=None, room_id=None, message=None):
        if room_id is not None:
            self.room_id = room_id
        if user_id is not None:
            self.user_id = user_id
        if message is not None:
            self.message = message


class User(EasyModel, base_db):
    __tablename__ = 'user'
    account = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    sid = db.Column(db.String(100), nullable=False)

    # 初始化
    def __init__(self, account, sid, password):
        self.account = account
        self.sid = sid
        self.password = password


class Room(EasyModel, base_db):
    __tablename__ = 'room'
    name = db.Column(db.String(10), nullable=False)

    # 初始化
    def __init__(self, name):
        self.name = name
