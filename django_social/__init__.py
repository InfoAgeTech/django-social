from __future__ import unicode_literals


class Source(object):
    DELICIOUS = 'DELICIOUS'
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'
    GOOGLEPLUS = 'GOOGLEPLUS'
    INSTAGRAM = 'INSTAGRAM'
    PICASA = 'PICASA'
    TWITTER = 'TWITTER'
    YOUTUBE = 'YOUTUBE'
    SOUNDCLOUD = 'SOUNDCLOUD'
    CHOICES = ((DELICIOUS, 'Delicious'),
               (FACEBOOK, 'Facebook'),
               (GOOGLE, 'Google'),
               (GOOGLEPLUS, 'Google+'),
               (INSTAGRAM, 'Instagram'),
               (PICASA, 'Picasa'),
               (SOUNDCLOUD, 'SoundCloud'),
               (TWITTER, 'Twitter'),
               (YOUTUBE, 'YouTube')
               )

    @classmethod
    def get_display(cls, source):
        """Gets the display value for a source."""
        if not source:
            return

        for k, display in cls.CHOICES:
            if k == source:
                return display

        return source
