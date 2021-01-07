from flask import g, request
from flask_restful import Resource

from app import db
from common.models.article import UserChannel
from common.utils.decorators import login_required


class ChannelUpdate(Resource):
    method_decorators = {'put': [login_required]}

    def put(self):
        user_id = g.user_id
        # request方法获取json中的数据
        channels = request.json.get('channels')
        # 更新数据库字段is_deleted为1,相当于全部逻辑删除
        UserChannel.query. \
            filter(UserChannel.user_id == user_id). \
            update({'is_deleted': 1})
        # 遍历channels列表,取出字典
        for channel in channels:
            channel_id = channel.get('id')
            new_seq = channel.get('seq')
            # 查询用户频道表中的频道信息
            user_channel = UserChannel.query. \
                filter(UserChannel.user_id == user_id, UserChannel.channel_id == channel_id). \
                first()
            # 如果有频道信息
            if user_channel:
                user_channel.sequence = new_seq
                user_channel.is_deleted = 0
            # 如果没有频道信息
            else:
                user_channel = UserChannel(user_id=g.user_id, channel_id=channel_id, sequence=new_seq)
                db.session.add(user_channel)
        db.session.commit()
        return {'channels': channels}
