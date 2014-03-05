from __future__ import unicode_literals

import unittest

from django.core.exceptions import ValidationError
from django_social import Source
from django_social.facebook.api import get_location_info
from django_social.facebook.api import search_places


class SocialTestCase(unittest.TestCase):

    def test_facebook_get_location_by_id(self):
        """
        Test for getting a location from facebook by it's ID.
        """
        location = get_location_info(location_id=120491747748)

        self.assertEqual(location.name, 'The Classic Cup')
        self.assertEqual(location.category, 'Restaurant/cafe')
        self.assertEqual(location.country, 'United States')
        self.assertEqual(location.latlong, (39.042173020445, -94.590903251913))
        self.assertEqual(location.line1, '301 W. 47th Street')
        self.assertEqual(location.line2, None)
        self.assertEqual(location.locality, 'Kansas City')
        self.assertEqual(location.phone, '816-753-1840')
        self.assertEqual(location.postal_code, '64112')
        self.assertEqual(location.source, Source.FACEBOOK)
        self.assertEqual(location.subdivision, 'MO')

    def test_places_search(self):
        """
        Test multiple places search from facebook.
        """
        with self.assertRaises(ValidationError) as e:
            search_places()
        self.assertEqual([u'One of the following args must be provided: query, latitude and longitude, or distance.'],
                          e.exception.messages)

        # Sometimes facebook gives back incorrect page sizes.  If I ask for 6,
        # I don't always get 6.
        places = search_places(query='coffee',
                               latitude=39.042173020445,
                               longitude=-94.590903251913,
                               distance=1000,
                               page_size=6)

        self.assertTrue(len(places) > 1)
