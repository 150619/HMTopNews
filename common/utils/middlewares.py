from flask import g, request
from common.utils.jwt_util import verify_jwt


def get_user_info():
    # 获取请求头中的token
    token = request.headers.get('Authorizations')
    # 如果登录
    if token:
        data = verify_jwt(token)
        # 校验token
        if data:
            g.user_id = data.get('user_id')
        # 校验失败
        else:
            g.user_id = None
    # 如果未登录
    else:
        g.user_id = None
