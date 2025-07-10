from flask import Blueprint

from apps.middleware.decorator import errorHandler

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/edit', methods=['post'])
@errorHandler
def edit(**kwargs):
    pass
