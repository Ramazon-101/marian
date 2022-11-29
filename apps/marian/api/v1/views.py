from ...models import Service, About
from rest_framework import viewsets
from .serializers import MarianSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    # http: // 127.0.0.1:8000/api/marian/v1/services/<id>
    queryset = Service.objects.all()
    serializer_class = MarianSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        MarianSerializer().set_model(Service)
        return serializer


class AboutViewSet(viewsets.ModelViewSet):
    # http: // 127.0.0.1:8000/api/marian/v1/about/<id>
    queryset = About.objects.all()
    serializer_class = MarianSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        MarianSerializer().set_model(About)
        return serializer
