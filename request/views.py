from rest_framework.generics import CreateAPIView

from request.serializers import RequestSerializer


class RequestCreateView(CreateAPIView):
    """
    Creates a request to add new study center
    """
    serializer_class = RequestSerializer


