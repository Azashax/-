from django.urls import path

from request.views import RequestCreateView

urlpatterns = [
    path('', RequestCreateView.as_view(), name='request'),
]
