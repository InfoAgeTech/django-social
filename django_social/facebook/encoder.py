import json
from .models import FacebookConnection


class FacebookConnectionEncoder(json.JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, FacebookConnection):
            return super(FacebookConnectionEncoder, self).default(obj)

        return obj.__dict__
