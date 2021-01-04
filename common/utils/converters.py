from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    regex = '1[3-9]\d{9}'


def register_converters(app):
    app.url_map.converters['MOBILE'] = MobileConverter
