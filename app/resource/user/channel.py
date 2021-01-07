from flask import g
from flask_restful import Resource

from common.models.article import UserChannel, Channel


class UserChannelResource(Resource):
    def get(self):
        # 定义字典列表
        channel_list = []
        if g.user_id:
            # 通过g对象获取user_id
            user_id = g.user_id
            # 数据库中联表查询,只需要Channel中的信息所以不用db.session.query(主表字段,从表字段)
            user_channels = Channel.query. \
                join(UserChannel, Channel.id == UserChannel.channel_id). \
                filter(user_id == UserChannel.user_id, UserChannel.is_deleted == 0). \
                order_by(UserChannel.sequence).all()
            # 用户没选择频道
            if len(user_channels) == 0:
                # 返回默认频道
                user_channels = Channel.query.filter(Channel.is_default == 1).all()
        # 未登录返回默认频道
        else:
            user_channels = Channel.query.filter(Channel.is_default == 1).all()
        # 返回列表,元素为所有符合查询的模型对象,遍历列表
        for user_channel in user_channels:
            # 转化为字典
            channel_dict = user_channel.to_dict()
            # 添加到列表拼接返回数据样式
            channel_list.append(channel_dict)
            # 添加推荐频道语法(指定位置,数据)
            channel_list.insert(0, {'id': 0, 'name': '推荐'})
        return {'channel': channel_list}
