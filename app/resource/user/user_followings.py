from datetime import datetime

from flask import request, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app import db
from common.models.user import User, Relation
from common.utils.decorators import login_required


class UserFollowings(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        parser = RequestParser()
        parser.add_argument('target', location='json', required=True, type=int)
        args = parser.parse_args()
        target = args.target
        user_id = g.user_id
        relation_ = Relation.query. \
            filter(Relation.user_id == g.user_id, Relation.author_id == target,
                   Relation.relation == Relation.RELATION.FOLLOW).all()
        relation__ = Relation.query. \
            filter(Relation.user_id == g.user_id, Relation.author_id == target,
                   Relation.relation == Relation.RELATION.BLACKLIST).all()
        relation___ = Relation.query. \
            filter(Relation.user_id == g.user_id, Relation.author_id == target,
                   Relation.relation == Relation.RELATION.DELETE).all()
        relation____ = Relation.query. \
            filter(Relation.user_id == g.user_id, Relation.author_id == target).all()
        # 没有关注信息则更新用户粉丝数关注数
        if not relation_:
            User.query. \
                filter(User.id == target). \
                update({'fans_count': User.fans_count + 1})
            User.query. \
                filter(User.id == user_id). \
                update({'following_count': User.following_count + 1})
            # 没有任何关系信息则添加关系信息
            if not relation____:
                relation = Relation(user_id=g.user_id, author_id=target, update_time=datetime.now(),
                                    relation=Relation.RELATION.FOLLOW)
                db.session.add(relation)
        else:
            return {'message': '已关注'}
        # 有黑名单关系或删除关系
        if relation__ or relation___:
            # 更新关注信息
            Relation.query. \
                filter(Relation.user_id == g.user_id, Relation.author_id == target). \
                update({'relation': Relation.RELATION.FOLLOW})
        db.session.commit()
        return {'target': target}
