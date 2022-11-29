from django.db.models import Q
from rest_framework import generics, viewsets, permissions
from .serializers import RoomSerializer, BookingSerialzier
from ...models import Room, Booking


class RoomViewSet(viewsets.ModelViewSet):
    # http://127.0.0.1:8000/api/room/v1/room/<id>/
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.request.method == ["GET"]:
            self.permission_classes = [permissions.AllowAny]
        elif self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = []
        return super(RoomViewSet, self).get_permissions()


class BookingCreateListView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/api/hotel/v1/room-create-list/
    queryset = Booking.objects.all()
    serializer_class = BookingSerialzier
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super(BookingCreateListView, self).get_queryset()
        check_in = self.request.POST.get('check_in')
        check_out = self.request.POST.get('check_out')
        if check_in and check_out:
            qs = qs.filter(~Q(go_date__range=[check_in, check_out]) or ~Q(back_date__range=[check_in, check_out]))
        return qs




    # def perform_create(self, serializer):
    #     serializer = self.serializer_class(data=self.request.data, context={"request": self.request})
    #     room = Room.objects.get(id=self.request.POST.get('room'))
    #     room.empty = True
    #     room.check_in = self.request.POST.get('go_date')
    #     room.check_out = self.request.POST.get('back_date')
    #     user_id = self.request.user.id
    #
    #     if serializer.is_valid():
    #         serializer.save(room=room, user_id=user_id)
    #         room.save()

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if self.request.method == 'GET':
    #         qs = BookingRooms.objects.filter(user_id=self.request.user.id)
    #     return qs