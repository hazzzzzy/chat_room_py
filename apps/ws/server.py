from datetime import datetime

from flask import request
from flask_socketio import emit

from apps import socketio
from apps.middleware.decorator import errorHandler
from apps.model.model import ChatHistory, Room
from utils.model2dict import model2dict

onlineUserAmount = 0
userDict = {}


@socketio.on('connect')
def handle_connect():
    global onlineUserAmount
    print(f'==========会话{request.sid}连接==========')
    onlineUserAmount += 1
    emit('countUser', {'onlineUserAmount': onlineUserAmount}, broadcast=True)
    # emit('sbOnline', {'username': request.sid}, broadcast=True, skip_sid=request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    global onlineUserAmount
    onlineUserAmount -= 1
    print(f'==========会话{request.sid}断开连接==========')
    emit('countUser', {'onlineUserAmount': onlineUserAmount}, broadcast=True)

    username = userDict.pop(sid, None)
    print(f"用户 {username}（{sid}）下线")
    emit('leave', {'sid': sid, 'username': username}, broadcast=True)


@socketio.on('join')
def handle_join(username):
    sid = request.sid
    userDict[sid] = username
    print(f"用户 {username}（{sid}）加入")
    # newUser = User(account=username, sid=sid)
    # newUser.save()

    emit('join', {'sid': sid, 'username': username}, broadcast=True, skip_sid=sid)


# @socketio.on('leave')
# def handle_leave(username):
#     sid = request.sid
#     username = userDict.pop(username, None)
#     print(f"用户 {username}（{sid}）下线")
#     emit('leave', {'username': username}, broadcast=True)


@socketio.on('sendMsg')
def sendMsg(msg):
    if not msg:
        emit('error', {'msg': '消息不能为空'})
    else:
        sid = request.sid
        print(f'会话 {request.sid} 发送消息：{msg}')
        newChatHistory = ChatHistory()
        emit('getMsg', {'msg': msg, 'sender': userDict[sid], 'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, broadcast=True)


@socketio.on('getHistory')
def getHistory():
    pass


# @socketio.on('getRoomList')
# def getRoomList():
#     room = Room.query.all()
#     room = [model2dict(i) for i in room]
#     emit('getRoomList', room)
