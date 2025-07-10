from flask import Blueprint

from apps.middleware.decorator import errorHandler
from apps.model.model import Room, User
from utils import R
from utils.model2dict import model2dict

rooms_bp = Blueprint('rooms_bp', __name__, url_prefix='/rooms')


@rooms_bp.route('/getList', methods=['get'])
@errorHandler
def getList(**kwargs):
    room = Room.query.all()
    if len(room) != 0:
        room = [model2dict(i) for i in room]

    avatarList = User.query.with_entities(User.id, User.avatar).all()
    if len(avatarList) != 0:
        avatarList = {i.id: i.avatar for i in avatarList}
    return R.ok({
        'room': room,
        'avatarList': avatarList,
    })

# @rooms_bp.route('/getHistory', methods=['get'])
# @errorHandler
# def getHistory(**kwargs):
#     roomID = request.args.get('roomID')
#     if not roomID:
#         return R.failed('房间ID不能为空')
#     history = (db.session.query(ChatHistory.create_at, ChatHistory.message, User.username)
#                .join(User, User.id == ChatHistory.user_id)
#                .filter(ChatHistory.room_id == roomID)
#                .all())
#     # username = '我' if username == userDict[sid]['username'] else username
#
#     return R.ok([{
#         'sendTime': i.create_at.strftime('%Y-%m-%d %H:%M:%S'),
#         'msg': i.message,
#         'sender': i.username
#     } for i in history])
