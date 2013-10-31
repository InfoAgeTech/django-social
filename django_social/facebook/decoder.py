from .models import FacebookConnection


def facebook_connection_decoder(obj):
    """This can be used in the object_hook for decoding a FacebookConnection
    object.
    """
    return FacebookConnection(user_id=obj.get('user_id'),
                              name=obj.get('name'))
