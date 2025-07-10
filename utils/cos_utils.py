import hashlib
import hmac

from qcloud_cos import CosConfig, CosS3Client

from config import COS_REGION, COS_SECRET_ID, COS_SECRET_KEY
from config import SECRET_KEY, COS_BUCKET

config = CosConfig(Region=COS_REGION, SecretId=COS_SECRET_ID, SecretKey=COS_SECRET_KEY, Token=None)
client = CosS3Client(config)


def useHmac(v: str) -> str:
    return hmac.new(SECRET_KEY.encode(), v.encode(), hashlib.sha256).hexdigest()


def cosUpload(file, path):
    response = client.put_object(
        Bucket=COS_BUCKET,
        Body=file,
        Key=path,
        EnableMD5=False
    )
    # todo：假如同对象名已存在但后缀不同，删除旧对象
    return response


def getAvatarList():
    marker = ""
    AvatarList = []
    while True:
        response = client.list_objects(
            Bucket=COS_BUCKET,
            Prefix='avatar/',
            Marker=marker,
            MaxKeys=10)
        if 'Contents' in response:
            for content in response['Contents']:
                AvatarList.append(content['Key'])
        if response['IsTruncated'] == 'false':
            break
        marker = response["NextMarker"]
    return AvatarList


if __name__ == '__main__':
    print(getAvatarList())
