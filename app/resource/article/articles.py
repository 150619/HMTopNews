from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.models.article import Article
from common.models.user import User


class Articles(Resource):
    def get(self):
        # 获取请求参数
        parser = RequestParser()
        parser.add_argument('channel_id', location='args')
        parser.add_argument('timestamp', location='args')
        args = parser.parse_args()
        channel_id = args.channel_id
        timestamp = args.timestamp
        from app import db
        article_list = db.session. \
            query(User.name, Article.user_id, Article.id, Article.comment_count, Article.title, Article.cover,
                  Article.ctime). \
            join(Article, User.id == Article.user_id). \
            filter(Article.channel_id == channel_id, Article.status == Article.STATUS.APPROVED,
                   Article.ctime < timestamp).all()
        results_list = []
        for article in article_list:
            article_dict = {
                'art_id': article.id,
                'title': article.title,
                'aut_id': article.user_id,
                'pubdate': article.ctime.isoformat(),
                'aut_name': article.name,
                'comm_count': article.comment_count,
                'cover': article.cover,
            }
            results_list.append(article_dict)
            # articles = [
            #     {
            #         'art_id': item.id,
            #         'title': item.title,
            #         'aut_id': item.user_id,
            #         'pubdate': item.ctime.isoformat(),
            #         'aut_name': item.name,
            #         'comm_count': item.comment_count,
            #         'cover': item.cover
            #     }
            # for item in article_list]
        return {'pre_timestamp': timestamp, 'results': results_list}
