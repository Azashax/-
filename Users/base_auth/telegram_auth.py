import json
import random
import string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User, UserProfile
from .token import create_token


class TelegramAuthAPIView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        data_user = check_telegram_user(data)
        # return Response(data=data_user, status=status.HTTP_201_CREATED)
        response = Response()
        response.data = data_user
        response.set_cookie(key='refresh', value=data_user['refresh'], httponly=True)
        response.status_code = status.HTTP_201_CREATED
        return response


def check_telegram_user(data):  # request,
    error_id = 'User not valid'
    if not data['password']:
    # if not data['hash']:
        return Response('Handle the missing Telegram data in the response.')
    user_id = validation(data, 'id', error_id)
    if user_id == error_id:
        return Response(data={'error': error_id}, status=status.HTTP_401_UNAUTHORIZED)
    email = validation(data, 'id', get_random(12)) + '@gmail.com'
    username = 'user' + validation(data, 'username', data['id'])
    last_name = validation(data, 'last_name', ' ')
    first_name = validation(data, 'first_name', ' ')
    gender = validation(data, 'gender', ' ')

    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.create(id=user_id, email=email, username=username,
                                        last_name=last_name, first_name=first_name,
                                        gender=gender,is_active=True)

    profile, profile_get = UserProfile.objects.get_or_create(user=user)
    avatar = validation(data, 'photo_url', False)
    if avatar and avatar != profile.photo_url:
        profile.photo_url = avatar
        profile.save()

    access_token = create_token(user.id, 1)
    refresh_token = create_token(user.id, 30)

    data = {
        'token': access_token,
        'refresh': refresh_token,
        'email': user.email,
        'name': user.first_name,
    }
    return data


def validation(data, key, default, typ=str):
    try:
        user_data = data[key]
    except Exception:
        user_data = default
    return typ(user_data)


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))