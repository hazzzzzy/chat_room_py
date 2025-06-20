from datetime import datetime


def msgConstant(msg, username='', role='user'):
    roleDict = {
        'user': '用户',
        'system': '系统消息',
        'admin': '管理员'
    }
    role = roleDict[role]
    if role != '用户':
        username = role
    return {'role': role, 'msg': msg, 'sender': username, 'sendTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
