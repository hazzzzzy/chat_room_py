from flask import Blueprint

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

# 注意：导入的是已经定义好的 login_bp、rooms_bp
from apps.views.login import login_bp
from apps.views.rooms import rooms_bp
from apps.views.upload import upload_bp
from apps.views.user import user_bp

# ✅ 必须先注册子蓝图
api_bp.register_blueprint(login_bp)
api_bp.register_blueprint(rooms_bp)
api_bp.register_blueprint(upload_bp)
api_bp.register_blueprint(user_bp)


def register_blueprint(app):
    app.register_blueprint(api_bp)
