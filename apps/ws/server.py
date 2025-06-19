from datetime import datetime

from flask import request
from flask_socketio import emit, join_room, leave_room

from apps import socketio
from apps.model.model import ChatHistory
from utils.getUser import getUser
from utils.model2dict import model2dict

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
    global onlineUserAmount
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
    emit('clientGetMsg', {
        'role': 'system',
        'sender': 'system',
        'msg': f'用户 {username} 已离开房间[{roomID}]',
        'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, room=roomID)
    emit('offline', {'sid': sid, 'username': userDetail['username']}, broadcast=True)


@socketio.on('serverJoinRoom')
def handleJoinRoom(data):
    global rooms
    sid = request.sid
    roomID = data.get('roomID')
    username = data.get('username')
    userID = data.get('userID')

    # 更新用户信息
    # userDict[sid] = {'username': username, 'userID': userID, 'room': roomID}
    userDict[sid] = {'username': username, 'userID': userID}
    # userDetail = rooms.get(roomID)

    rooms[roomID] = [userID] if rooms.get(roomID) is None else rooms[roomID].append(userID)
    join_room(room=roomID, sid=sid)
    print(f"用户 {username}（{sid}）加入房间 {roomID}")

    emit('online', {'sid': sid, 'username': username}, broadcast=True, skip_sid=sid)
    emit('clientJoinRoom', {'sid': sid, 'username': username, 'roomID': roomID}, room=roomID)


@socketio.on('serverLeaveRoom')
def handleLeaveRoom(data):
    roomID = data.get('roomID')

    global rooms
    sid = request.sid
    userID, username = getUser(userDict, sid)

    rooms[roomID].remove(userID)
    leave_room(sid=sid, room=roomID)
    emit('clientGetMsg', {
        'role': 'system',
        'sender': 'system',
        'msg': f'用户 {username} 已离开房间[{roomID}]',
        'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, room=roomID)
    print(f"用户 {username} 已离开房间[{roomID}]")


@socketio.on('serverSendMsg')
def sendMsg(data):
    msg = data['msg']
    roomID = data['roomID']
    if not msg:
        emit('error', {'msg': '消息不能为空'})
    else:
        sid = request.sid
        userID, username = getUser(userDict, sid)
        print(f'{username} 给房间 {roomID} 发送消息：{msg}')
        newChatHistory = ChatHistory(userID, roomID, msg)
        newChatHistory.save()
        emit('clientGetMsg',
             {'role': 'user', 'msg': msg, 'sender': username, 'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
             room=roomID)


# @socketio.on('getHistory')
# def getHistory(roomID):
#     history = ChatHistory.query.filter_by(roomID=roomID).all()
#     history = [model2dict(i) for i in history]
#     emi

# @socketio.on('getRoomList')
# def getRoomList():
#     room = Room.query.all()
#     room = [model2dict(i) for i in room]
#     emit('getRoomList', room)
