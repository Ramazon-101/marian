from django.urls import path, include
from .views import ServiceViewSet, AboutViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'services', ServiceViewSet)
router.register(r'about', AboutViewSet)

urlpatterns = [
    path('', include(router.urls))
]
