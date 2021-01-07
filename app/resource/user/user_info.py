from flask_restful import Resource

from common.utils.decorators import login_required


class UserInfoResource(Resource):
    method_decorators = {'get': [login_required]}

    def get(self):
        # 找到已登录用户的id
        from flask import g
        user_id = g.user_id
        from common.models.user import User
        from sqlalchemy.orm import load_only
        # 通过当前登录用户id从数据库中查询
        user_info = User.query. \
            options(load_only(User.id, User.name, User.profile_photo, User.introduction, User.article_count,
                              User.following_count, User.fans_count)). \
            filter(user_id == User.id).first()
        return user_info.to_dict()
