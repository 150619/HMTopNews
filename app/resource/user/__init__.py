from flask import Blueprint
from flask_restful import Api
from common.utils.output import output_json
from app.resource.user import passport, user_info, channel_update, channel
from common.utils.constants import BASE_URL_PREFIX

# 创建蓝图对象
user_bp = Blueprint('user', __name__, url_prefix=BASE_URL_PREFIX)
# 将蓝图对象包装成具备restful风格的的组件对象
user_api = Api(user_bp)
user_api.representation('application/json')(output_json)
# 给类视图增加信息
user_api.add_resource(passport.SMSCodeResource, '/sms/codes/<MOBILE:mobile>')
user_api.add_resource(passport.LoginResource, '/authorizations')
user_api.add_resource(user_info.UserInfoResource, '/user')
user_api.add_resource(channel_update.ChannelUpdate, '/user/channels')
user_api.add_resource(channel.UserChannelResource, '/user/channels')
