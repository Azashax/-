from django.utils import timezone
from django.conf import settings

from rest_framework import authentication
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Refresh'

    @staticmethod
    def verify_token(token):
        try:
            decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception:
            return None
        exp = decode_data['exp']
        if timezone.now().timestamp() > exp:
            return False

        return True
