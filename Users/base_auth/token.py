import jwt
from django.utils.timezone import timedelta
from django.utils import timezone
from django.conf import settings
from ..models import User


def create_token(user_id: int, time):
    payload = {
        'id': user_id,
        'exp': timezone.now() + timedelta(time),
        'iat': timezone.now(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
