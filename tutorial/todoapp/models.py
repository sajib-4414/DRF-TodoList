from django.db import models


# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    user_created = models.CharField(max_length=100)

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data

