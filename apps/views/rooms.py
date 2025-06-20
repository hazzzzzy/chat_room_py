from flask import Blueprint, request

from apps.middleware.decorator import errorHandler
from apps.model.model import Room, ChatHistory, User
from extensions import db
from utils import R
from utils.model2dict import model2dict

rooms_bp = Blueprint('rooms_bp', __name__, url_prefix='/rooms')


@rooms_bp.route('/getList', methods=['get'])
@errorHandler
def getList():
    room = Room.query.all()
    room = [model2dict(i) for i in room]
    if len(room) == 0:
        return R.failed('房间列表为空')
    return R.ok(room)


@rooms_bp.route('/getHistory', methods=['get'])
@errorHandler
def getHistory():
    roomID = request.args.get('roomID')
    if not roomID:
        return R.failed('房间ID不能为空')
    history = (db.session.query(ChatHistory.create_at, ChatHistory.message, User.account)
               .join(User, User.id == ChatHistory.user_id)
               .filter(ChatHistory.room_id == roomID)
               .all())

    return R.ok([{
        'sendTime': i.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        'msg': i.message,
        'sender': i.account
    } for i in history])
