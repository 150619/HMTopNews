from flask import Blueprint
from flask_restful import Api

from app.resource.channel import all_channel
from common.utils.constants import BASE_URL_PREFIX
from common.utils.output import output_json

# 创建蓝图对象
channel_bp = Blueprint('channel', __name__, url_prefix=BASE_URL_PREFIX)
# 创建api对象
channel_api = Api(channel_bp)
# 转换成restful风格
channel_api.representation('application/json')(output_json)
# 添加路由
channel_api.add_resource(all_channel.AllChannel, '/channels')
