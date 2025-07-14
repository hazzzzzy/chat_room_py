from flask import Blueprint, request

from apps.middleware.decorator import errorHandler
from apps.model.model import User
from extensions import db
from utils import R

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/edit', methods=['post'])
@errorHandler
def edit(**kwargs):
    userID = kwargs['userID']
    data = request.get_json()
    username = data.get('username')
    if not username:
        return R.failed(msg='用户名不能为空')
    user = User.query.with_entities(User.id, User.username).all()
    if len(user) == 0:
        return R.failed(msg='没有用户数据，请联系管理员')
    isUserExist = [i for i in user if str(i.id) == userID]
    if len(isUserExist) == 0:
        return R.failed(msg='用户不存在')
    isUsernameExist = [i for i in user if i.username == username and i.id != userID]
    if len(isUsernameExist) > 0:
        return R.failed(msg='用户名已存在')
    User.query.filter_by(id=userID).update({'username': username})
    db.session.commit()
    return R.ok(msg='用户名修改成功')
