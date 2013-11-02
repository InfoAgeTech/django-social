# -*- coding: utf-8 -*-
from django.template import Library
from ..facebook.models import FacebookConnection

register = Library()


@register.filter
def fb_avatar_url(facebook_user_id=None):
    """
    Currency formatting template filter.

    Takes a number -- integer, float, decimal -- and formats it according to
    the locale specified as the template tag argument (arg). Examples:

      * {{ value|currency }}
      * {{ value|currency:"en_US" }}
      * {{ value|currency:"pt_BR" }}
      * {{ value|currency:"pt_BR.UTF8" }}

    If the argument is omitted, the default system locale will be used.

    The third parameter, symbol, controls whether the currency symbol will be
    printed or not. Defaults to true.

    As advised by the Django documentation, this template won't raise
    exceptions caused by wrong types or invalid locale arguments. It will
    return an empty string instead.

    Be aware that currency formatting is not possible using the 'C' locale.
    This function will fall back to 'en_US.UTF8' in this case.
    """
    if not facebook_user_id:
        return ''
    fb_connection = FacebookConnection(user_id=facebook_user_id, name=None)
    return fb_connection.get_avatar_url()
