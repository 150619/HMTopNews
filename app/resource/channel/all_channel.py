from flask_restful import Resource
from sqlalchemy.orm import load_only

from common.models.article import Channel


class AllChannel(Resource):
    def get(self):
        channel_list = []
        # 从数据库查询所有频道
        all_channels = Channel.query.options(load_only(Channel.id, Channel.name)).all()
        # 遍历列表
        for all_channel in all_channels:
            all_channel_dict = all_channel.to_dict()
            # 添加列表形成restful风格
            channel_list.append(all_channel_dict)
        return {'channels': channel_list}
