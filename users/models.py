from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    challenger = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

