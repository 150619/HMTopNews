from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only

from app import db
from common.models.user import User, Relation
from common.utils.decorators import login_required


class UserUnfollow(Resource):
    method_decorators = {'delete': [login_required]}

    def delete(self, target):
        user_id = g.user_id
        # 判断关系是否为关注关系
        relation = Relation.query. \
            options(load_only(Relation.user_id, Relation.author_id, Relation.relation)). \
            filter(Relation.user_id == user_id, Relation.author_id == target,
                   Relation.relation == Relation.RELATION.FOLLOW).all()
        if not relation:
            return {'message': '用户未关注'}
        else:
            # 粉丝数减少
            User.query. \
                filter(User.id == target). \
                update({'fans_count': User.fans_count - 1})
            # 关注数减少
            User.query. \
                filter(User.id == user_id). \
                update({'following_count': User.following_count - 1})
            # 修改用户关系
            Relation.query. \
                filter(Relation.user_id == user_id, Relation.author_id == target). \
                update({'relation': Relation.RELATION.DELETE})
            db.session.commit()
            return target
