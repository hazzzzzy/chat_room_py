from flask import Blueprint

from apps.middleware.decorator import errorHandler
from apps.model.model import Room
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
