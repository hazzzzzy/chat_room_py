from flask import request, Blueprint

from apps.model.model import User
from utils import R

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['post'])
def login():
    data = request.get_json()
    user = data.get('account')
    pwd = data.get('password')
    if not user or not pwd:
        return R.failed('缺少账号或密码')
    user = User.query.filter_by(account=user).first()
    if not user:
        return R.failed('查无此人')
    elif user.password != pwd:
        return R.failed('密码不对')
    return R.ok({
        'account': user.account,
        'userID': user.id
    })
