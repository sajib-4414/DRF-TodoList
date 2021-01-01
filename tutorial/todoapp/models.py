from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

class TodoItem(models.Model):
    PRIORITIES = Choices(
       (1, 'CRITICAL', _('Critically important')),
       (2, 'VERY_HIGH', _('Very important')),
       (3, 'HIGH', _('Highly important')),
        (4, 'MEDIUM', _('Medium important')),
        (5, 'LOW', _('Low important')),
   )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    due_datetime = models.DateTimeField(null=True,blank=True)
    remind_me_datetime = models.DateTimeField(null=True,blank=True)
    priority = models.PositiveSmallIntegerField(
       choices=PRIORITIES,
       default=PRIORITIES.LOW,
   )
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True)
    # the reason why user is null is, we do not want to take user input from the user,
    # instead it will be populated from the request

    def __str__(self):
        data = (self.title[:30] + '..') if len(self.title) > 30 else self.title
        return data
