import redis

redisClient = redis.Redis(host='127.0.0.1', port=6379, db=0, password=None, socket_connect_timeout=5)


def redisSet(k, v, expire=0):
    """
    Set a key-value pair in Redis with an expiration time.
    :param k: Key to set.
    :param v: Value to set.
    :param expire: Expiration time in seconds (default is 60 seconds).
    """
    if expire == 0:
        redisClient.set(k, v)
    else:
        redisClient.set(k, v, ex=expire)


def redisGet(k):
    """
    Get the value of a key from Redis.
    :param k: Key to retrieve.
    :return: Value associated with the key, or None if the key does not exist.
    """
    v = redisClient.get(k)
    if v is None:
        return None
    return v.decode('utf-8')  # Decode bytes to string


def redisDelete(k):
    """
    Delete a key from Redis.
    :param k: Key to delete.
    """
    redisClient.delete(k)


if __name__ == '__main__':
    print(redisGet('test_key'))
