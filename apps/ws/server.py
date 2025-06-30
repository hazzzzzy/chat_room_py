import copy
import json

from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect

from apps import socketio
from apps.constants.constants import msgConstant, errorMsgConstant
from apps.model.model import ChatHistory, User
from extensions import db
from utils.jwt_instance import verify_jwt
from utils.redis_instance import redisSet, redisGet

onlineUsersKey = 'cr:ws:oluser'
roomsKey = 'cr:ws:rooms'


def getValue(k):
    data = redisGet(k)
    if not data:
        return None
    data = json.loads(data)
    return data


def setValue(k, v):
    v = json.dumps(v, ensure_ascii=False)
    redisSet(k, v)


def getOnlineAmount():
    _ = getValue(roomsKey)
    if not _:
        return 0
    return sum(len(set(users)) for users in _.values())


def getRoomOnlineAmount(roomID):
    _ = getValue(roomsKey)
    if not _:
        return 0
    if roomID not in _:
        return 0
    return len(set(_[roomID]))


@socketio.on('connect')
def handle_connect(auth):
    sid = request.sid
    # 鉴权
    token = auth.get('token')
    if not token:
        emit('error', errorMsgConstant(msg='用户未登录，无法连接服务器，请重新登录'))
        disconnect()
        return
    currentUser, result = verify_jwt(token.removeprefix('Bearer '))
    if not result:
        emit('error', errorMsgConstant(msg=currentUser))
        disconnect()
        return

    # 更新在线用户
    isBroadcast = True
    users = getValue(onlineUsersKey)
    if users:
        users[sid] = currentUser
        setValue(onlineUsersKey, users)
        # 断开同账号在线连接
        for existSID, existUser in users.items():
            if existSID != sid and existUser['userID'] == currentUser['userID']:
                isBroadcast = False
                emit('error', errorMsgConstant(msg='链接断开，同账号用户已上线'), room=existSID)
                disconnect(sid=existSID)
        newUser = getValue(onlineUsersKey)
        newUser[sid] = currentUser
        setValue(onlineUsersKey, newUser)
    else:
        setValue(onlineUsersKey, {sid: currentUser})
    if isBroadcast:
        emit('online', {'username': currentUser['username']}, broadcast=True, include_self=False)
    print(f'==========会话[{request.sid}]连接==========')
    print(f'用户[{currentUser["username"]}]上线')


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    users = getValue(onlineUsersKey)
    usersCopy = copy.deepcopy(users)
    rooms = getValue(roomsKey)
    user = users.pop(sid)
    if not user:
        emit('error', errorMsgConstant(msg='断联接口报错，请联系管理员'))
        return
    setValue(onlineUsersKey, users)

    username = user['username']
    userID = user['userID']
    roomID = str(user.get('roomID'))
    # 删除该用户房间信息并离开房间
    if roomID:
        roomID = str(roomID)
        rooms[roomID].remove(userID)
        setValue(roomsKey, rooms)
        leave_room(room=roomID, sid=sid)
        emit('clientGetMsg', msgConstant(
            msg=f'用户[{username}]已离开房间',
            username=username,
            role='system'
        ), room=roomID)

    emit('countUser', {'onlineUserAmount': getOnlineAmount()}, broadcast=True)

    isBroadcast = True
    for s, u in usersCopy.items():
        if u['userID'] == userID:
            isBroadcast = False
    if isBroadcast:
        emit('offline', {'username': username}, broadcast=True)
    print(f"用户[{username}]下线了")
    print(f'==========会话[{request.sid}]断开连接==========')


@socketio.on('serverJoinRoom')
def handleJoinRoom(data):
    sid = request.sid
    newRoomID = str(data['roomID'])
    username = data['username']
    userID = data['userID']

    users = getValue(onlineUsersKey)
    rooms = getValue(roomsKey) or {}

    # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    # print('before join ', users)
    # print('before join ', rooms)

    # 检查用户是否已在其他房间中，在则退出
    oldRoomID = users[sid].get('roomID')
    if oldRoomID:
        oldRoomID = str(oldRoomID)  # 确保oldRoomID是字符串类型
        rooms[oldRoomID].remove(userID)
        leave_room(sid=sid, room=oldRoomID)
        # 广播离开房间消息
        emit('clientGetMsg', msgConstant(
            msg=f'用户[{username}]已离开房间',
            username=username,
            role='system'
        ), room=oldRoomID)
        emit('clientCountRoomUser', {'onlineRoomUserAmount': getRoomOnlineAmount(oldRoomID)}, room=oldRoomID)
        print(f"用户[{username}]离开房间[{oldRoomID}]")

    # 更新用户信息
    users[sid] = {'username': username, 'userID': userID, 'roomID': newRoomID}
    setValue(onlineUsersKey, users)

    # 更新房间信息
    if newRoomID not in rooms:
        rooms[newRoomID] = [userID]
    else:
        rooms[newRoomID].append(userID)
    # 更新房间内用户信息
    setValue(roomsKey, rooms)
    # print('after join ', users)
    # print('after join ', rooms)

    # 加入新房间
    join_room(room=newRoomID, sid=sid)
    print(f"用户[{username}]进入房间[{newRoomID}]")
    emit('countUser', {'onlineUserAmount': getOnlineAmount()}, broadcast=True)

    # 把推送历史消息放到这里
    history = (db.session.query(ChatHistory.create_at, ChatHistory.message, User.username)
               .join(User, User.id == ChatHistory.user_id)
               .filter(ChatHistory.room_id == newRoomID)
               .all())
    emit('clientGetHistory', [{
        'sendTime': i.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        'msg': i.message,
        'sender': i.username
    } for i in history])
    # 广播进入房间消息
    emit('clientGetMsg', msgConstant(
        msg=f'用户[{username}]已进入房间',
        username=username,
        role='system'
    ), room=newRoomID)
    emit('clientJoinRoom', {'room': newRoomID})
    emit('clientCountRoomUser', {'onlineRoomUserAmount': getRoomOnlineAmount(newRoomID)}, room=newRoomID)


@socketio.on('serverSendMsg')
def sendMsg(msg):
    if not msg:
        emit('error', errorMsgConstant(msg='消息不能为空'))
    else:
        sid = request.sid
        users = getValue(onlineUsersKey)
        user = users[sid]
        # print('msg:', user)
        username = user['username']
        userID = user['userID']
        roomID = user.get('roomID')

        if not all([userID, username, roomID]):
            emit('error', errorMsgConstant(msg='用户信息缺失，请刷新页面重新链接'))
            disconnect()
            return
        print(f'用户[{username}]给房间[{roomID}]发送消息：{msg}')
        newChatHistory = ChatHistory(userID, roomID, msg)
        newChatHistory.save()
        emit('clientGetMsg',
             msgConstant(msg=msg, username=username),
             room=roomID)
