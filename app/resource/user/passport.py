import random
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.utils.constants import SMS_CODE_EXPIRE


class SMSCodeResource(Resource):
    def get(self, mobile):
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 手机号:验证码的形式保存到redis数据库
        key = f'{mobile}'
        from app import redis_client
        redis_client.set(key, sms_code, ex=SMS_CODE_EXPIRE)
        print(f'mobile:{mobile},sms_code:{sms_code}')
        return {'mobile': mobile}

    def post(self):
        # 创建请求解析器对象
        parser = RequestParser()
        # 添加参数规则
        # parser.add_argument(['mobile', 'code'], location='json')
        parser.add_argument('mobile', location='json')
        parser.add_argument('code', location='json')
        # 执行解析
        args = parser.parse_args()
        # 获取参数
        mobile = args.mobile
        code = args.code
        from app import redis_client
        key = f'{mobile}'
        r_code = redis_client.get(key)
        if r_code != code:
            return {'message': 'failure', 'data': None}, 400
