from flask_restful import Resource

from app import db
from common.models.article import Article, ArticleContent
from common.models.user import User


class ArticleInfo(Resource):
    # 可以不登陆访问,所以用g.user_id是否存在判断用户是否登录
    # method_decorators = {'get': [login_required]}

    def get(self, article_id):
        article_info = db.session. \
            query(Article.id, Article.title, Article.ctime, Article.user_id, User.name, User.profile_photo,
                  ArticleContent.content). \
            join(User, Article.user_id == User.id). \
            join(ArticleContent, Article.id == ArticleContent.article_id). \
            filter(Article.id == article_id).first()
        # article_info = db.session. \
        #     query(Article.id, Article.title, Article.ctime, Article.user_id, User.name, User.profile_photo,
        #           ArticleContent.content). \
        #     join(User, Article.user_id == User.id). \
        #     join(ArticleContent, Article.id == ArticleContent.article_id). \
        #     filter(Article.id == article_id).first()
        result = {
            'art_id': article_info.id,
            'title': article_info.title,
            'pubdate': article_info.ctime.isoformat(),
            'aut_id': article_info.user_id,
            'aut_name': article_info.name,
            'aut_photo': article_info.profile_photo,
            'content': article_info.content
        }
        return result
