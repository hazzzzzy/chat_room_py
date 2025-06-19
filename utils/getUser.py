def getUser(userDict, sid):
    user = userDict[sid]
    username = user.get('username')
    userID = user.get('userID')
    return userID, username
