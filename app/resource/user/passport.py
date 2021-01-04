import random
from flask_restful import Resource

from common.utils.constants import SMS_CODE_EXPIRE


class SMSCodeResource(Resource):
    def get(self, mobile):
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 手机号:验证码的形式保存到redis数据库
        key = mobile
        from app import redis_client
        redis_client.set(key, sms_code, ex=SMS_CODE_EXPIRE)
        print(f'mobile:{mobile},sms_code:{sms_code}')
        return {'mobile': mobile}
