from django.urls import path, include
from .views import RoomViewSet, BookingCreateListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'room', RoomViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('room-create-list/', BookingCreateListView.as_view()),
]