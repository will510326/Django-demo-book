from pyexpat import model
from django.db import models

# Create your models here.


class NewsUnit(models.Model):
    catego = models.CharField(max_length=10, null=False)
    nickname = models.CharField(max_length=20, null=False)
    title = models.CharField(max_length=50, null=False)
    message = models.TextField(null=False)
    pubtime = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=False)
    press = models.IntegerField(default=0)

    def __str__(self):
        return self.title
