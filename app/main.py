from flask import jsonify

from app import create_app

app = create_app('dev')


@app.route('/')
def index():
    rule_dict = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(rule_dict)
