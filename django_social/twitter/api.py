# -*- coding: utf-8 -*-
from twython import Twython

 
def get_profile_pic(twitter_username, size='bigger'):
    """
    Gets the twitter user avatar.
    """
    t = Twython()
    return t.getProfileImageUrl(twitter_username, size=size)