from django.db import models
from django.utils import timezone


# Status:
#   - 0: creating
#   - 1: in progress
#   - 2: terminated
class Dashboard(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    beginning = models.DateField(default=timezone.now())
    deadline = models.DateField()
    participants = models.IntegerField()
    author = models.TextField()
