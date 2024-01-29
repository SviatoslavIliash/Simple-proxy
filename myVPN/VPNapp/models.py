from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static


class CustomUser(AbstractUser):
    info = models.CharField(max_length=200, verbose_name="info")
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="image")

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return static('VPNapp/images/default_image.jpg')


class MySite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30, unique=True)
    alias_url = models.URLField(max_length=250, unique=True)
    visit_counter = models.IntegerField(default=0)
    data_in = models.IntegerField(default=0)
    data_out = models.IntegerField(default=0)

    def __str__(self):
        return self.alias + ' ' + self.alias_url
