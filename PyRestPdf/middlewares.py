import django.core.exceptions
from django.conf import settings


class InvalidToken(django.core.exceptions.SuspiciousOperation):
    """Invalid characters in kiosk key"""

    pass


class NoToken(django.core.exceptions.PermissionDenied):
    """No token"""

    pass


class TokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dumb_custom_header = request.headers.get("Dumb-Token", None)
        if dumb_custom_header and dumb_custom_header[:7] == "Bearer ":
            dumb_custom_token = dumb_custom_header[7:]
            if dumb_custom_token == settings.WRITE_TOKEN:
                setattr(request, "custom_rights", "w")
            elif dumb_custom_token == settings.READ_TOKEN:
                setattr(request, "custom_rights", "r")
            else:
                raise InvalidToken()
        else:
            raise NoToken()
        return self.get_response(request)
