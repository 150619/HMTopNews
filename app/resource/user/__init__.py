from flask import Blueprint
from flask_restful import Api
from common.utils.output import output_json
from .passport import SMSCodeResource

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)
user_api.representation('application/json')(output_json)
user_api.add_resource(SMSCodeResource, '/sms/codes')
