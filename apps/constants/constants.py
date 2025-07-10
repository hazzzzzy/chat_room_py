from datetime import datetime


def msgConstant(msg, senderID=None, username='', role='user'):
    roleDict = {
        'user': '用户',
        'system': '系统消息',
        'admin': '管理员'
    }
    role = roleDict[role]
    if role != '用户':
        username = role
    return {'role': role, 'msg': msg, 'senderID': senderID, 'sender': username, 'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


def errorMsgConstant(code=0, msg='操作失败'):
    return {
        'code': code,
        'msg': msg,
    }
