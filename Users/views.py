from datetime import datetime, timedelta
import random
import string
import jwt

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated)


from .authentication import IsAuthenticatedCustom
from .backends import JWTAuthentication
from .models import User, Jwt
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer, AllUsersSerializers, RefreshSerializer, UserProfileSerializer)


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    data_token = {
        # 'id': payload,
        'id': payload['id'],
        'username': payload['username'],
        'first_name': payload['first_name'],
        "photo_url": payload["photo_url"] ,
        'exp': timezone.now() + timedelta(days=1000000),
        'iat': timezone.now()
    }
    token = jwt.encode(data_token, settings.SECRET_KEY, algorithm='HS256')
    return token


def get_refresh_token(payload):
    data_token = {
        'id': payload,
        'exp': timezone.now() + timedelta(days=30),
        'iat': timezone.now()
    }
    token = jwt.encode(data_token, settings.SECRET_KEY, algorithm='HS256')
    return token


class RegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            token = get_access_token(payload=data)
            return Response({'Successful': 'User save', 'data': data, 'token': token}, status=status.HTTP_201_CREATED)
        else:
            data = serializer.data
            if User.objects.filter(username=data['username']).exists():
                return Response({'error': 'A user with the same email or username already exists'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': 'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response({'errors': 'endpoint "register/users/" not method GET'})
    

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.data
            user = authenticate(
                email=data['username'],
                password=data['password']
            )
            username = data["username"]
            if user is None:
                return Response({'error': 'User not found!'}, status=status.HTTP_401_UNAUTHORIZED)
            Jwt.objects.filter(user_id=user.id).delete()
            response = Response()
            refresh = get_refresh_token(user.id)
            access = get_access_token(user.id)
            Jwt.objects.create(
                user_id=user.pk, access=access, refresh=refresh
            )
            response.set_cookie(key='auth', value=refresh, httponly=True, samesite='none') #  , samesite=None
            response.status_code = status.HTTP_200_OK
            response.data = {
                'username': username,
                'access': access,
                'refresh': refresh
            }
            return response
        else:
            return Response({'error': 'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        """
        Принимает
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"]
            )
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status=400)
        life_token = JWTAuthentication.verify_token(active_jwt.refresh)
        if life_token:
            return self.refresh_jwt(active_jwt)
        return Response({'error': 'User UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)        

    def refresh_jwt(self, active_jwt):
        access = get_access_token(active_jwt.user.id)
        refresh = get_refresh_token(active_jwt.user.id)

        active_jwt.access = access  # .decode()
        active_jwt.refresh = refresh  # .decode()
        active_jwt.save()

        response = Response()
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        response.status_code = 200
        response.data = {
            "access": access,
            'refresh': refresh
        }
        return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        user_id = request.user.id
        Jwt.objects.filter(user_id=user_id).delete()
        response = Response()
        response.delete_cookie(key='refresh')
        response.status_code = 200
        response.data = "logged out successfully"

        return response


class AllUsers(ListAPIView):
    serializer_class = AllUsersSerializers
    queryset = User.objects.all()


class AllUsers2(ListAPIView):
    serializer_class = AllUsersSerializers
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return self.request.user


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return self.request.user