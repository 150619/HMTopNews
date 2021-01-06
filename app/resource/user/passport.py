from datetime import datetime, timedelta

import random
from flask import current_app

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from common.models.user import User
from common.utils.jwt_util import generate_jwt


class SMSCodeResource(Resource):
    def get(self, mobile):
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 手机号:验证码的形式保存到redis数据库
        key = f'{mobile}'
        from app import redis_client
        from common.utils.constants import SMS_CODE_EXPIRE
        redis_client.set(key, sms_code, ex=SMS_CODE_EXPIRE)
        print(f'mobile:{mobile},sms_code:{sms_code}')
        return {'mobile': mobile}


class LoginResource(Resource):
    def post(self):
        # 创建请求解析器对象
        parser = RequestParser()
        # 添加参数规则
        parser.add_argument('mobile', location='json', required=True)
        parser.add_argument('code', location='json', required=True)
        # 执行解析
        args = parser.parse_args()
        # 获取参数
        mobile = args.mobile
        code = args.code
        from app import redis_client
        key = f'{mobile}'
        # 从redis数据库获取验证码
        r_code = redis_client.get(key)
        # 如果验证码不存在或验证码不相等
        if not r_code or r_code != code:
            return {'message': 'failure', 'data': None}
        user = User.query.options(load_only(User.mobile)).filter(User.mobile == mobile).first()
        # 如果用户存在记录最后一次登陆时间
        if user:
            user.last_login = datetime.now()
        # 如果不存在注册新用户,用户名字为手机号
        else:
            user = User(mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
        db.session.commit()
        token = generate_jwt({'user_id': user.id},
                             expiry=datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS']))
        return {'token': token}
