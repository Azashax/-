import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission
from .models import User


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        print(request.COOKIES)
        try:
            user = decodeJWT(request.META['HTTP_AUTHORIZATION'])
        except Exception:
            return False
        if not user:
            return False
        request.user = user
        if request.user and request.user.is_authenticated:
            return True
        return False
        

def decodeJWT(bearer):
    if not bearer:
        return None
    token = bearer[7:]
    decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    if decoded:
        try:
            return User.objects.get(id=decoded["id"])
        except Exception:
            return None