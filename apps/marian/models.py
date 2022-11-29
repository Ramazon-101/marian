from django.db import models


class About(models.Model):
    title = models.CharField(max_length=212)
    description = models.TextField()
    image = models.ImageField(upload_to='About')

    def __str__(self):
        return self.title


class  Service(models.Model):
    service_icon = models.ImageField(upload_to='Service_icon')
    service_title = models.CharField(max_length=212)
    image = models.ImageField(upload_to='Service')
    service_content = models.TextField()

    def __str__(self):
        return self.service_title
