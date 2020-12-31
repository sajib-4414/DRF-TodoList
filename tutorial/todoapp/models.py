from django.db import models
from django.contrib.auth.models import AbstractUser, User


class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data
