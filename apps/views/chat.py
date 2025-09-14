from flask import request, Blueprint

from utils import R
from utils.R import agnoStreamOk
from utils.agent_instance import mysql_sql_agent

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/chat')

@chat_bp.route('/chat', methods=['get'])
# @errorHandler
def chat(**kwargs):
    q = request.args.get('q')
    if not q:
        return R.failed(msg='需要传入问题')
    user_id = kwargs.get('user_id')
    agno_response = mysql_sql_agent.run(input=q, user_id=user_id, stream=True)
    return agnoStreamOk(agno_response)
