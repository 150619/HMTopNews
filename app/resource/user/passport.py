from flask_restful import Resource


class SMSCodeResource(Resource):
    def get(self):
        return {'a': 'a'}
