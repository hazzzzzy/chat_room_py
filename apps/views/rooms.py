from flask import Blueprint, request

from apps.middleware.decorator import errorHandler
from apps.model.model import Room, ChatHistory
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
    history = ChatHistory.query.filter_by(roomID=roomID).all()
    history = [model2dict(i) for i in history]
    if len(history) == 0:
        return R.failed('房间列表为空')
    return R.ok(history)
