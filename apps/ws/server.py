from flask import request
from flask_socketio import emit, join_room, leave_room

from apps import socketio
from apps.constants.constants import msgConstant
from apps.model.model import ChatHistory
from utils.getUser import getUser

onlineUserAmount = 0
userDict = {}
rooms = {}


@socketio.on('connect')
def handle_connect():
    global onlineUserAmount
    print(f'==========会话{request.sid}连接==========')
    onlineUserAmount += 1
    emit('countUser', {'onlineUserAmount': onlineUserAmount}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    global onlineUserAmount, userDict, rooms
    onlineUserAmount -= 1
    print(f'==========会话{request.sid}断开连接==========')
    emit('countUser', {'onlineUserAmount': onlineUserAmount}, broadcast=True)

    # 删除该在线用户信息
    userDetail = userDict.pop(sid)
    if not userDetail:
        emit('error', {'msg': '断联接口报错，请联系管理员'})
        return
    roomID = userDetail['roomID']
    username = userDetail['username']
    userID = userDetail['userID']
    print(f"用户 {username}（{sid}）下线")
    # 删除该用户房间信息
    rooms[roomID].remove(userID)
    leave_room(room=roomID, sid=sid)
    emit('clientGetMsg', msgConstant(
        msg=f'用户 {username} 已离开房间',
        username=username,
        role='system'
    ), room=roomID)
    emit('offline', {'sid': sid, 'username': userDetail['username']}, broadcast=True)


@socketio.on('serverJoinRoom')
def handleJoinRoom(data):
    global rooms, userDict

    sid = request.sid
    newRoomID = data['roomID']
    username = data['username']
    userID = data['userID']

    if sid not in userDict:
        # 更新用户信息
        emit('online', {'username': username}, broadcast=True, skip_sid=sid)
    else:
        # 检查用户是否已在其他房间中，在则退出
        oldRoomID = userDict[sid].get('roomID')
        if oldRoomID:
            rooms[oldRoomID].remove(userID)
            leave_room(sid=sid, room=oldRoomID)
            # 广播离开房间消息
            emit('clientGetMsg', msgConstant(
                msg=f'用户 {username} 已离开房间',
                username=username,
                role='system'
            ), room=oldRoomID)
            print(f"用户 {username}（{sid}）离开房间 {oldRoomID}")
            # 广播离开房间消息
            # emit('clientLeaveRoom', {'room': newRoomID})

    userDict[sid] = {'username': username, 'userID': userID, 'roomID': newRoomID}
    if newRoomID not in rooms:
        rooms[newRoomID] = [userID]
    else:
        rooms[newRoomID].append(userID)
    join_room(room=newRoomID, sid=sid)
    print(f"用户 {username}（{sid}）进入房间 {newRoomID}")
    # 广播进入房间消息
    emit('clientGetMsg', msgConstant(
        msg=f'用户 {username} 已进入房间',
        username=username,
        role='system'
    ), room=newRoomID)
    # 广播进入房间消息
    emit('clientJoinRoom', {'room': newRoomID})


@socketio.on('serverSendMsg')
def sendMsg(data):
    global userDict
    msg = data
    if not msg:
        emit('error', {'msg': '消息不能为空'})
    else:
        sid = request.sid
        userID, username, roomID = getUser(userDict, sid)
        if not all([userID, username, roomID]):
            emit('error', {'msg': '用户信息缺失，请重新登录'})
            return
        print(f'{username} 给房间 {roomID} 发送消息：{msg}')
        newChatHistory = ChatHistory(userID, roomID, msg)
        newChatHistory.save()
        emit('clientGetMsg',
             msgConstant(msg=msg, username=username),
             room=roomID)
