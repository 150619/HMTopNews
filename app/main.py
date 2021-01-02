from flask import jsonify

from app import create_app

# 通过工厂方法创建app
app = create_app('dev')


# 定义视图函数绑定路由信息
@app.route('/')
def index():
    rule_dict = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(rule_dict)
