import datetime
import json

import jwt

# --- 1. 定义一个用于签名的密钥 ---
# 在实际应用中，这个密钥应该是长而复杂的随机字符串，并且绝不能泄露！
# 可以通过 os.urandom(24).hex() 生成
SECRET_KEY = "6202ee63b@0c2463bae3!40e8765a481f1"


# --- 2. 模拟用户登录，生成 JWT ---
def generate_jwt(data):
    """
    模拟用户登录成功后，服务器生成 JWT。
    """
    # Header (头部) - PyJWT 会自动处理
    # Payload (载荷) - 包含用户的身份信息和过期时间
    data = json.dumps(data, ensure_ascii=False, indent=4)
    payload = {
        'data': data,
        # "is_admin": is_admin,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60 * 60 * 12),
        # "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=Config.JWT_EXPIRE_TIME),
        "iat": datetime.datetime.now(datetime.timezone.utc),  # 签发时间
        "iss": "chatWave"  # 签发者
    }

    # 使用 HS256 算法和密钥对 JWT 进行签名
    # encode 方法会返回编码后的 JWT 字符串
    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt


# --- 3. 模拟接收请求，验证 JWT ---
def verify_jwt(token):
    """
    模拟服务器收到请求后，验证 JWT。
    """
    try:
        # 使用相同的密钥和算法来解码和验证 JWT
        # decode 方法会同时验证签名和 exp (过期时间)
        decoded_payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],  # 指定允许的算法
            issuer="chatWave"  # 验证签发者
        )
        data = decoded_payload.get('data')  # 获取载荷中的数据
        if data:
            # 如果数据是 JSON 字符串，解析它
            decoded_payload['data'] = json.loads(data)
        else:
            raise jwt.InvalidTokenError('JWT 载荷中缺少data字段')
        return decoded_payload['data'], True

    except jwt.ExpiredSignatureError:
        # print("JWT 令牌已过期。")
        return "JWT 令牌已过期", False
    except jwt.InvalidTokenError as e:
        # print(f"无效的 JWT 令牌: {e}")
        return f'无效的 JWT 令牌: {e}', False


# --- 4. 运行示例 ---
if __name__ == "__main__":
    print("--- JWT 生成示例 ---")
    user_id = 123
    username = "test_user"
    is_admin = False

    # 生成一个 JWT
    token = generate_jwt({'user_id': user_id, 'username': username, 'is_admin': is_admin})
    print(f"生成的 JWT: {token}\n")

    print("--- JWT 验证示例 (有效令牌) ---")
    # 验证这个有效的 JWT
    payload, is_valid = verify_jwt(token)
    if is_valid:
        print(f"JWT 验证成功！\n载荷内容: {payload}")
    else:
        print("JWT 验证失败。")

    print("\n--- JWT 验证示例 (模拟过期令牌) ---")
    # 模拟一个过期令牌：我们将创建一个过期时间很短的令牌
    expired_payload = {
        "user_id": 456,
        "username": "expired_user",
        "exp": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=5),  # 5秒前就过期了
        "iat": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1),
        "iss": "your-app-issuer"
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm="HS256")
    print(f"模拟的过期 JWT: {expired_token}")

    # 尝试验证过期令牌
    payload_expired, is_valid_expired = verify_jwt(expired_token)
    if is_valid_expired:
        print(f"JWT 验证成功！\n载荷内容: {payload_expired}")
    else:
        print("JWT 验证失败（预期是过期）。")

    print("\n--- JWT 验证示例 (模拟篡改令牌) ---")
    # 模拟篡改令牌：故意修改 Payload 的某个字符
    tampered_token = token + "X"  # 随意修改一个字符
    print(f"模拟的篡改 JWT: {tampered_token}")

    # 尝试验证篡改令牌
    payload_tampered, is_valid_tampered = verify_jwt(tampered_token)
    if is_valid_tampered:
        print(f"JWT 验证成功！\n载荷内容: {payload_tampered}")
    else:
        print("JWT 验证失败（预期是无效签名）。")

    print("\n--- JWT 验证示例 (模拟不同密钥) ---")
    # 模拟不同密钥验证：用错误的密钥验证
    WRONG_SECRET_KEY = "wrong-secret-key"
    try:
        jwt.decode(token, WRONG_SECRET_KEY, algorithms=["HS256"], issuer="your-app-issuer")
        print("错误密钥验证成功 (这不应该发生)。")
    except jwt.InvalidSignatureError:
        print("JWT 验证失败：签名无效 (预期是密钥不匹配)。")
    except jwt.InvalidTokenError as e:
        print(f"JWT 验证失败：其他无效令牌错误 ({e})。")
