def getUser(userDict, sid):
    user = userDict[sid]
    username = user.get('username')
    userID = user.get('userID')
    roomID = user.get('roomID')
    return userID, username, roomID
