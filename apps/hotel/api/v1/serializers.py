from rest_framework import serializers
from ...models import Room, Booking, Wallet


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'image', 'price', 'duration']


class BookingSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'adults', 'children', 'capacity', 'go_date', 'back_date']
        extra_kwargs = {
            'user': {'required': False, 'allow_null': True},
            'room': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        booking = Booking.objects.create(user_id=user.id, **validated_data)
        booking.save()
        return booking

    def validate(self, attrs):
        attrs = dict(attrs)
        room = Room.objects.get(title=attrs.get('room'))
        obj = Wallet.objects.get(author=self.context['request'].user)
        if room.price > obj.balance:
            raise serializers.ValidationError({"money": "you don't have enough money"})
        elif room.price == obj.balance:
            obj.balance = 0
        else:
            obj.balance -= room.price // 2
        obj.save()
        return attrs

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     check_in = attrs.get('check_in')
    #     check_out = attrs.get('check_out')
    #     booking = Booking.objects.filter(check_in=check_in, check_out=check_out, user_id=user.id)
    #     if booking:
    #         raise serializers.ValidationError({'detail': 'this room has booked already'})
    #     return attrs
