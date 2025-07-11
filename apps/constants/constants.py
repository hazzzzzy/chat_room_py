from datetime import datetime


def msgConstant(msg, msgID=None, senderID=None, sender=None, role=2, sendTime=None):
    roleDict = {
        1: 'admin', 2: 'user', 3: 'system'
    }
    return {'id': msgID,
            'role': roleDict[role],
            'msg': msg,
            'senderID': senderID,
            'sender': sender,
            'sendTime': sendTime or datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


def errorMsgConstant(code=0, msg='操作失败'):
    return {
        'code': code,
        'msg': msg,
    }
