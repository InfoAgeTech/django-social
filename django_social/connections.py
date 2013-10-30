# -*- coding: utf-8 -*-
import json


class FacebookConnection(object):
    """
    Represents a facebook user connection.

    :param user_id: the user id for the connection (related to the specific
        social connection type)
    :param name: name of the user connection (i.e. "John Doe")
    """
    user_id = None
    name = None

    def __init__(self, user_id, name, *args, **kwargs):
        self.user_id = user_id
        self.name = name

    def get_avatar_url(self):
        """
        Gets a square users facebook avatar url 50x50
        """
        return self.get_profile_pic(pic_type='square')

    def get_profile_pic(self, pic_type='large'):
        """
        :param pic_type: should be one of
            - 'square' (50x50) default
            - 'small' (50 pixels wide, variable height)
            - 'normal' (100 pixels wide, variable height), and
            - 'large' (about 200 pixels wide, variable height):

        Note: This url can be http or https.  Probably want to flex this based
        on if I'm using SSL or not.
        """
        return 'http://graph.facebook.com/{facebook_user_id}/picture?type={pic_type}'.format(facebook_user_id=self.user_id,
                                                                                             pic_type=pic_type)


class FacebookConnectionEncoder(json.JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, FacebookConnection):
            return super(FacebookConnectionEncoder, self).default(obj)

        return obj.__dict__


def facebook_connection_decoder(obj):
    return FacebookConnection(user_id=obj.get('user_id'),
                              name=obj.get('name'))
