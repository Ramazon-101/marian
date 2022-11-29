from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.hotel.api.v1.urls'))
]
