import json

from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect

from apps import socketio
from apps.constants.constants import msgConstant
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
    print('count', _)
    return sum(len(users) for users in _.values())


@socketio.on('connect')
def handle_connect(auth):
    sid = request.sid
    # 鉴权
    token = auth.get('token')
    if not token:
        emit('error', {'msg': '用户未登录，无法连接服务器，请重新登录'})
        disconnect()
        return
    user, result = verify_jwt(token.removeprefix('Bearer '))
    if not result:
        emit('error', {'msg': user})
        disconnect()
        return
    # 更新在线用户
    users = getValue(onlineUsersKey)
    if not users:
        setValue(onlineUsersKey, {sid: user})
    else:
        users[sid] = user
        setValue(onlineUsersKey, users)
    emit('online', {'username': user['username']}, broadcast=True, skip_sid=sid)
    print(f'==========会话{request.sid}连接==========')
    print(f'用户[{user["username"]}]上线')


@socketio.on('disconnect')
def handle_disconnect(_):
    # 删除该在线用户信息
    sid = request.sid
    users = getValue(onlineUsersKey)
    rooms = getValue(roomsKey)
    user = users.pop(sid)
    setValue(onlineUsersKey, users)
    if not user:
        emit('error', {'msg': '断联接口报错，请联系管理员'})
        return
    username = user['username']
    userID = user['userID']
    roomID = str(user.get('roomID'))
    # print(type(rooms), rooms)
    # print(type(roomID), roomID)
    # print(type(userID), userID)
    if roomID:
        # 删除该用户房间信息
        rooms[roomID].remove(userID)
        setValue(roomsKey, rooms)
        leave_room(room=roomID, sid=sid)
        emit('clientGetMsg', msgConstant(
            msg=f'用户[{username}]已离开房间',
            username=username,
            role='system'
        ), room=roomID)

    emit('countUser', {'onlineUserAmount': getOnlineAmount()}, broadcast=True)
    emit('offline', {'username': username}, broadcast=True)
    print(f"用户[{username}]下线")
    print(f'==========会话{request.sid}断开连接==========')


@socketio.on('serverJoinRoom')
def handleJoinRoom(data):
    sid = request.sid
    newRoomID = str(data['roomID'])
    username = data['username']
    userID = data['userID']

    users = getValue(onlineUsersKey)
    rooms = getValue(roomsKey) or {}
    print('before join ', users)
    print('before join ', rooms)

    # 检查用户是否已在其他房间中，在则退出
    # todo: 多开一个窗口，离开房间后会删除第一条数据
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
        emit('clientCountRoomUser', {'onlineRoomUserAmount': len(rooms[oldRoomID])}, room=oldRoomID)
        print(f"用户[{username}]离开房间[{oldRoomID}]")

    # 更新用户信息
    users[sid] = {'username': username, 'userID': userID, 'roomID': newRoomID}
    setValue(onlineUsersKey, users)

    # 更新房间信息
    if newRoomID not in rooms:
        rooms[newRoomID] = [userID]
    else:
        if userID not in rooms[newRoomID]:
            rooms[newRoomID].append(userID)

    # 更新房间内用户信息
    setValue(roomsKey, rooms)
    print('after join ', users)
    print('after join ', rooms)

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
    emit('clientCountRoomUser', {'onlineRoomUserAmount': len(rooms[newRoomID])}, room=newRoomID)


@socketio.on('serverSendMsg')
def sendMsg(msg):
    if not msg:
        emit('error', {'msg': '消息不能为空'})
    else:
        sid = request.sid
        users = getValue(onlineUsersKey)
        user = users[sid]
        print('msg:', user)
        username = user['username']
        userID = user['userID']
        roomID = user.get('roomID')

        if not all([userID, username, roomID]):
            emit('error', {'msg': '用户信息缺失，请刷新页面重新链接'})
            disconnect()
            return
        print(f'用户[{username}]给房间[{roomID}]发送消息：{msg}')
        newChatHistory = ChatHistory(userID, roomID, msg)
        newChatHistory.save()
        emit('clientGetMsg',
             msgConstant(msg=msg, username=username),
             room=roomID)
