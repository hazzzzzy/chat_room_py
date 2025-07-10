import os

from flask import Blueprint
from flask import request, jsonify

from apps.middleware.decorator import errorHandler
from apps.model.model import User
from config import COS_BASE_URL
from config import MAX_CONTENT_LENGTH, COS_BUCKET
from extensions import db
from utils import R
from utils.cos_utils import cosUpload, useHmac

upload_bp = Blueprint('upload_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


# def failUpload(msg='上传失败', status_code=400):
#     """通用失败响应"""
#     result = {
#         "code": -1,
#         "msg": msg,
#     }
#     return jsonify(result), status_code


def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generateCosPath(filename, user_id):
    """生成COS存储路径"""
    ext = filename.rsplit('.', 1)[1].lower()
    user_id = useHmac(user_id)
    return f"avatar/{user_id}.{ext}"


@upload_bp.route('/upload', methods=['post'])
@errorHandler
def upload(**kwargs):
    userID = kwargs['userID']
    # 检查请求内容类型
    if 'file' not in request.files:
        return R.failed(msg='无文件上传')

    file = request.files['file']

    # 检查是否选择了文件
    if file.filename == '':
        return R.failed(msg='文件名不能为空')

    # 验证文件类型和大小
    if not allowed_file(file.filename):
        return R.failed(msg=f'不支持的文件类型，请上传 {"/".join(ALLOWED_EXTENSIONS)} 格式的图片')

    # 在内存中检查文件大小（避免保存到磁盘）
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)  # 重置文件指针
    if file_length > MAX_CONTENT_LENGTH:
        return R.failed(msg=f'文件大小超过限制，最大允许上传{MAX_CONTENT_LENGTH / (1024 * 1024)}MB')
    path = generateCosPath(file.filename, userID)
    r = cosUpload(file, path)
    User.query.filter_by(id=userID).update({'avatar': COS_BASE_URL + path})
    db.session.commit()
    return R.ok(data=COS_BASE_URL + path)
