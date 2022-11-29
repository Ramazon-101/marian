from django.conf import settings
from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=221)
    image = models.ImageField(upload_to='room/')
    price = models.IntegerField()
    duration = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    adults = models.IntegerField()
    children = models.IntegerField()
    capacity = models.IntegerField()
    go_date = models.DateTimeField(auto_now_add=False)
    back_date = models.DateTimeField(auto_now_add=False)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return self.author.username