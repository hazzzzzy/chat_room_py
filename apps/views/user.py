from flask import Blueprint, request

from apps.forms.user import addUserForm, editUserForm, banUserForm
from apps.middleware.decorator import errorHandler
from apps.model.model import User
from extensions import db
from utils import R
from utils.getFormError import getError
from utils.model2dict import model2dict

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/edit', methods=['post'])
@errorHandler
def edit(**kwargs):
    myUserID = kwargs['userID']
    myUser = User.query.filter_by(id=myUserID).first()
    if not myUser or myUser.is_admin != 1 or myUser.is_delete == 1 or myUser.status != 1:
        print('edit接口权限：', myUser or model2dict(myUser))
        return R.failed(msg='无权限操作或管理员用户状态异常')

    form = editUserForm(request.form)
    if not form.validate():
        return R.failed(msg=getError(form))

    username = form.username.data
    isUsernameExist = User.query.filter(User.username == username, User.is_delete == 2, User.id != form.userID.data).first()
    if isUsernameExist:
        return R.failed(msg='用户名已存在')
    user = User.query.filter_by(id=form.userID.data, is_delete=2).first()
    if not user:
        return R.failed(msg='用户不存在')
    for i, j in form.data.items():
        if j is not None:
            setattr(user, i, j)
    db.session.commit()
    # 更新redis中在线用户的用户名
    # user = redisGet('cr:ws:oluser')
    # if user:
    #     user = json.loads(user)
    #     for k, v in user.items():
    #         if v.get(userID) == userID:
    #             user[k]['username'] = username
    #             user = json.dumps(user, ensure_ascii=False)
    #             redisSet('cr:ws:oluser', user)
    #             break
    return R.ok(msg='用户名修改成功')


@user_bp.route('/getList', methods=['get'])
@errorHandler
def getList(**kwargs):
    users = User.query.filter_by(is_delete=2).all()
    if not users:
        return R.failed(msg='没有用户数据，请联系管理员')
    user_list = []
    for i in users:
        user = model2dict(i)
        del user['password']  # 移除密码字段
        del user['is_delete']
        del user['token']
        user_list.append(user)
    return R.ok(data=user_list)


@user_bp.route('/add', methods=['post'])
@errorHandler
def add(**kwargs):
    myUserID = kwargs['userID']
    myUser = User.query.filter_by(id=myUserID).first()
    if not myUser or myUser.is_admin != 1 or myUser.is_delete == 1 or myUser.status != 1:
        print('add接口权限：', myUser or model2dict(myUser))
        return R.failed(msg='无权限操作或管理员用户状态异常')

    form = addUserForm(request.form)
    if not form.validate():
        return R.failed(msg=getError(form))

    username = form.username.data
    isUsernameExist = User.query.filter_by(username=username, is_delete=2).first()
    if isUsernameExist:
        return R.failed(msg='用户名已存在')
    account = form.account.data
    isAccountExist = User.query.filter_by(account=account, is_delete=2).first()
    if isAccountExist:
        return R.failed(msg='账号已存在')
    newUser = User(account=account, password=form.password.data, username=username)
    newUser.save()
    return R.ok()


@user_bp.route('/delete', methods=['post'])
@errorHandler
def delete(**kwargs):
    myUserID = kwargs['userID']
    myUser = User.query.filter_by(id=myUserID).first()
    if not myUser or myUser.is_admin != 1 or myUser.is_delete == 1 or myUser.status != 1:
        print('del接口权限：', myUser or model2dict(myUser))
        return R.failed(msg='无权限操作或用户状态异常')

    data = request.get_json()
    userID = data.get('userID')
    if not userID:
        return R.failed(msg='用户ID不能为空')
    user = User.query.filter_by(id=userID).first()
    if not user:
        return R.failed(msg='用户不存在')
    if user.is_admin == 1:
        return R.failed(msg='无法删除管理员')
    user.is_delete = 1
    db.session.commit()
    return R.ok(msg='用户删除成功')


@user_bp.route('/detail', methods=['get'])
@errorHandler
def detail(**kwargs):
    userID = request.args.get('userID')
    if not userID:
        return R.failed(msg='用户ID不能为空')
    user = User.query.filter_by(id=userID).first()
    if not user:
        return R.failed(msg='没有用户数据，请联系管理员')
    elif user.is_delete == 1:
        return R.failed(msg='用户已被删除')
    user = model2dict(user)
    del user['password']  # 移除密码字段
    del user['is_delete']
    del user['token']
    return R.ok(data=user)


@user_bp.route('/ban', methods=['post'])
@errorHandler
def ban(**kwargs):
    myUserID = kwargs['userID']
    myUser = User.query.filter_by(id=myUserID).first()
    if not myUser or myUser.is_admin != 1 or myUser.is_delete == 1 or myUser.status != 1:
        print('ban接口权限：', myUser or model2dict(myUser))
        return R.failed(msg='无权限操作或用户状态异常')

    form = banUserForm(request.form)
    if not form.validate():
        return R.failed(msg=getError(form))

    user = User.query.filter_by(id=form.userID.data).first()
    if not user:
        return R.failed(msg='没有用户数据，请联系管理员')
    elif user.is_delete == 1:
        return R.failed(msg='用户已被删除')
    user.status = form.status.data
    db.session.commit()
    return R.ok(msg='用户状态修改成功')
