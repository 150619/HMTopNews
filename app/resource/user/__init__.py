from flask import Blueprint
from flask_restful import Api
from common.utils.output import output_json
from .passport import SMSCodeResource

# 创建蓝图对象
user_bp = Blueprint('user', __name__)
# 将蓝图对象包装成具备restful风格的的组件对象
user_api = Api(user_bp)
user_api.representation('application/json')(output_json)
# 给类视图增加信息
user_api.add_resource(SMSCodeResource, '/sms/codes/<MOBILE:mobile>')
