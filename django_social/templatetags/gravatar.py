# -*- coding: utf-8 -*-
"""
Minor modificationss taken from 
http://code.google.com/p/django-gravatar/source/browse/trunk/gravatar/templatetags/gravatar.py

Examples:

"""

from django import template
from django.conf import settings
from django.utils.html import escape

import hashlib
import urllib

GRAVATAR_URL_PREFIX = getattr(settings, "GRAVATAR_URL_PREFIX", "http://www.gravatar.com/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE", "")

register = template.Library()


def gravatar_for_email(email, size=32):
    url = "%savatar/%s/?" % (GRAVATAR_URL_PREFIX, hashlib.md5(email).hexdigest())
    url += urllib.urlencode({"s": str(size), "default": GRAVATAR_DEFAULT_IMAGE})
    return escape(url)


def gravatar_img_for_email(email, size=32):
    url = gravatar_for_email(email, size)
    return escape(url)


def gravatar(user, size=32):
    # backward compatibility
    if hasattr(user, 'email'):
        return gravatar_img_for_email(email=user.email, size=size)
    # elif hasattr(user, 'email'):
    return gravatar_img_for_email(email=user, size=size)


register.simple_tag(gravatar)
register.simple_tag(gravatar_for_email)
register.simple_tag(gravatar_img_for_email)
