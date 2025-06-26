from flask import request, Blueprint

from apps.middleware.decorator import errorHandler
from apps.model.model import User
from utils import R
from utils.jwt_instance import generate_jwt
from utils.redis_instance import redisGet

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['post'])
@errorHandler
def login(**kwargs):
    data = request.get_json()
    account = data.get('account')
    pwd = data.get('password')
    if not account or not pwd:
        return R.failed('缺少账号或密码')
    user = User.query.filter_by(account=account).first()
    username = user.username
    userID = user.id
    if not user:
        return R.failed('查无此人')
    elif user.password != pwd:
        return R.failed('密码错误')

    token = generate_jwt({'userID': userID, 'username': username})
    if not token:
        return R.failed('生成token失败，请稍后再试')
    return R.ok({
        'username': username,
        'userID': userID,
        'token': token
    })


@login_bp.route('/test', methods=['get'])
def test(**kwargs):
    print(redisGet('cr:ws:oluser'))
    return '', 200
