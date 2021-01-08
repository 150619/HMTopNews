from flask import Blueprint
from flask_restful import Api

from app.resource.article import articles, article_info
from common.utils.constants import BASE_URL_PREFIX
from common.utils.output import output_json

article_bp = Blueprint('article', __name__, url_prefix=BASE_URL_PREFIX)
article_api = Api(article_bp)
article_api.representation('application/json')(output_json)
article_api.add_resource(articles.Articles, '/articles')
article_api.add_resource(article_info.ArticleInfo, '/articles/<article_id>')
