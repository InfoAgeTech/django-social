# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ValidationError
from django_geo.models import Location
from django_social import Source
from python_tools.api import get_json_api_contents
from urllib2 import urlopen
from urlparse import urljoin
import urllib

APP_ACCESS_TOKEN_API_URL = u'https://graph.facebook.com/oauth/access_token?{0}'
FRIENDS_API_URL = u'https://graph.facebook.com/{facebook_user_id}/friends?{params}'
USER_API_URL = u'https://graph.facebook.com/{facebook_user_id}?{params}'
LOCATION_API_URL = u'https://graph.facebook.com/{location_id}?{query_params}'
SEARCH_API_URL = u'https://graph.facebook.com/search?{0}'
USER_PHOTO_API_URL = u'http://graph.facebook.com/{facebook_user_id}/picture?type={pic_type}'
DEFAULT_METADATA_FIELDS = ('email', 'gender', 'birthday', 'username',
                           'location', 'significant_other', 'timezone',
                           'picture', 'locale', 'currency')


def get_friends(facebook_user_id, access_token, datatype=None):
    """
    Get a list of users friends.

    :param datatype: the format datatype to return.  If None, this will be
        FacebookConnection objects.  If format == 'json', this will return
        json.
    """
    params = {'access_token': access_token}
    friends_api_url = urljoin(FRIENDS_API_URL.format(
                                            facebook_user_id=facebook_user_id,
                                            params=urllib.urlencode(params)))

    connections = get_json_api_contents(friends_api_url)
    friend_list = connections.get('data', [])
    friend_list.sort(key=lambda k: k.get('name'))

    if datatype == 'json':
        return friend_list

    from django_social.facebook.models import FacebookConnection
    fb_connections = []

    for friend in friend_list:
        fb_connections.append(FacebookConnection(user_id=friend.get('id'),
                                                 name=friend.get('name')))

    return fb_connections


def get_user_metadata(facebook_user_id, access_token, fields=None):
    """
    Gets metadata about a user.

    Additional metadata about the user can be defined in the metadata fields. If
    you want all metadata fields returned, set "fields" param to be None.

    @see: https://developers.facebook.com/docs/reference/api/
    """
    if not fields:
        fields = DEFAULT_METADATA_FIELDS

    params = {'access_token': access_token,
              'fields': u','.join(fields)}

    metadata_api_url = urljoin(USER_API_URL.format(
                                            facebook_user_id=facebook_user_id,
                                            params=urllib.urlencode(params)))

    user_metadata = get_json_api_contents(metadata_api_url)
    return user_metadata


def get_location_info(location_id, source=Source.FACEBOOK):
    """
    Gets location information by location id.

    :param location_id: external source location id of the location.
    :param source: the source of the information.  (i.e. facebook, etc)

    Example facebook response:

    {
        "id": "112213565457929",
        "name": "Overland Park, Kansas",
        "location": {
           "city": "Overland Park",
           "state": "KS",
           "country": "United States",
           "latitude": 38.9401,
           "longitude": -94.6807
    }

    Converted into an Address object.
    :return: Address object or None if no location is found.

    """
    if not location_id:
        return None

    query_params = {'fields': 'location,name,category,phone',
                    'access_token': get_app_access_token()}

    location_api_url = LOCATION_API_URL.format(
                                 location_id=location_id,
                                 query_params=urllib.urlencode(query_params))

    location_info = get_json_api_contents(location_api_url)
    location = location_info.get('location', {})

    if not location:
        return None

    return Location.objects.get_or_create(
        ext_id=location_info.get('id'),
        source=source,
        defaults={
            'name': location_info.get('name'),
            'line1': location.get('street'),
            'locality': location.get('city'),
            'subdivision': location.get('state'),
            'country': location.get('country'),
            'postal_code': location.get('zip'),
            'latitude': location.get('latitude'),
            'longitude': location.get('longitude'),
            'category': location_info.get('category'),
            'phone': location_info.get('phone'),
            'ext_id': location_info.get('id'),
            'source': 'FACEBOOK'
        }
    )[0]


def search_places(query=None, latitude=None, longitude=None, distance=None,
                  page=1, page_size=25):
    """
    Gets places nearby a latitude and longitude point.  One or more of the
    following must be present or a ValidationError will be thrown:

        - query
        - latitude and longitude
        - distance

    :param query: query string to search for
    :param latitude: latitude of a point to search for.
    :param longitude: longitude of a point to search for.
    :param distance: distance in feet to search for places from the latitude,
        longitude point.

    Sample facebook response:

    {
       "data": [
          {
             "name": "The Classic Cup",
             "location": {
                "street": "301 W. 47th Street",
                "city": "Kansas City",
                "state": "MO",
                "country": "United States",
                "zip": "64112",
                "latitude": 39.042173020445,
                "longitude": -94.590903251913
             },
             "category": "Restaurant/cafe",
             "id": "120491747748"
          },
          {
             "name": "Houston's Restaurant - Country Club Plaza",
             "location": {
                "street": "4640 Wornall Rd",
                "city": "Kansas City",
                "state": "MO",
                "country": "United States",
                "zip": "64112",
                "latitude": 39.042480096479,
                "longitude": -94.590150525498
             },
             "category": "Restaurant/cafe",
             "id": "231025796770"
          },
          {
             "name": "McCormick & Schmick's Seafood Restaurant - Kansas City, MO",
             "location": {
                "street": "448 West 47th Street",
                "city": "Kansas City",
                "state": "MO",
                "country": "United States",
                "zip": "64112",
                "latitude": 39.042536412504,
                "longitude": -94.593036414391
             },
             "category": "Restaurant/cafe",
             "id": "155854511155677"
          },
          ...
       ],
       "paging": {
          "next": "https://graph.facebook.com/search?type=place&center=39.041446,-94.590518&distance=1000&access_token=AAAAAAITEghMBALtpMSCzb9RO9ZA74ZB41l67RLMzR2xzRDV8btVgfmle7xPKYY928QdHjYjuXJlurZBH68hygnU1XZBU8sWn9sUL1xxlfQZDZD&limit=25&offset=25&__after_id=48204942945"
       }
    }
    """
    if not query and (not latitude or not longitude) and not distance:
        raise ValidationError('One of the following args must be provided: query, latitude and longitude, or distance.')

    query_params = {'type': 'place',
                    'access_token': get_app_access_token(),
                    'limit': page_size,
                    'offset': (page - 1) * page_size}

    if query:
        query_params['q'] = query

    if latitude and longitude:
        query_params['center'] = '{0},{1}'.format(latitude, longitude)

    if distance:
        query_params['distance'] = distance

    api_url = SEARCH_API_URL.format(urllib.urlencode(query_params))

    location_info = get_json_api_contents(api_url)
    places = location_info.get('data', [])
    return places


def get_user_photo(facebook_user_id, pic_type='large'):
        """
        :param pic_type: should be one of
            - 'square' (50x50) default
            - 'small' (50 pixels wide, variable height)
            - 'normal' (100 pixels wide, variable height), and
            - 'large' (about 200 pixels wide, variable height):

        Note: This url can be http or https.  Probably want to flex this based
        on if I'm using SSL or not.
        """
        return USER_PHOTO_API_URL.format(facebook_user_id=facebook_user_id,
                                         pic_type=pic_type)


def get_app_access_token():

    access_token = getattr(settings, 'FACEBOOK_ACCESS_TOKEN', None)

    if access_token:
        return access_token

    query_params = {'client_id': settings.FACEBOOK_APP_ID,
                    'client_secret': settings.FACEBOOK_API_SECRET,
                    'grant_type': 'client_credentials'}

    api_url = APP_ACCESS_TOKEN_API_URL.format(urllib.urlencode(query_params))

    access_token = urlopen(api_url).read()
    access_token = access_token.split('=')[1]
    return access_token
