# -*- coding: utf-8 -*-
from python_dates.parsers import parse_datetime
from python_tools.api import get_json_api_contents


def get_bookmarks(delicious_username, tag=None):
    """
    Returns a list of recent bookmarks from delicious
    
    @see http://feeds.delicious.com/v2/json/troygrosfield
    
    Example bookmark:
    [
        {
            "a": "troygrosfield",
            "d": "HTML5 input type=number and decimals/floats in Chrome « Isotoma Blog",
            "n": "As you may already know, HTML5 has introduced a number of new input types, one of which is the “number” type. As you might expect, this is a form field which accepts numeric input. So what happens in Chrome with the following HTML when we try to enter a decimal (floating point) number and submit the form?",
            "u": "http://blog.isotoma.com/2012/03/html5-input-typenumber-and-decimalsfloats-in-chrome/",
            "t": [
                "html5"
            ],
            "dt": "2012-10-12T22:24:15Z"
        },
        ...
    ]
    """
    if tag:
        api_url = u"http://feeds.delicious.com/v2/json/{0}/{1}".format(delicious_username,
                                                                       tag)
    else:
        api_url = u"http://feeds.delicious.com/v2/json/{0}".format(delicious_username)

    bookmarks = get_json_api_contents(api_url)
    for bookmark in bookmarks:
        if bookmark.get('dt'):
            bookmark['dt'] = parse_datetime(bookmark.get('dt'))
    return bookmarks


def get_bookmarks_by_tag(delicious_username, tag):
    """
    Gets delicious bookmarks by a specific tag.
    """
    return get_bookmarks(delicious_username, tag)
