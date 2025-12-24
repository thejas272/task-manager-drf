from django.db import models

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  email = models.EmailField(unique=True)


class TaskModel(models.Model):
  owner = models.ForeignKey(User,on_delete=models.CASCADE, null=False, blank=False)

  title       = models.CharField(max_length=300,null=False, blank=False)
  description = models.TextField(null=True, blank=True)
  status      = models.BooleanField(default=False)

  due_date    = models.DateField(null=True, blank=True)
  created_at  = models.DateTimeField(auto_now_add=True)
  updated_at  = models.DateTimeField(auto_now=True) 


  class Meta:
    constraints = [models.UniqueConstraint(fields=['owner','title'],
                                           name='unique_task_per_user'
                                          )
                  ]


  def __str__(self):
    return f"task - '{self.title}' of user - '{self.owner.username}'"
  
  def save(self,*args,**kwargs):
    if not self.due_date:
      self.due_date = timezone.now().date() + timedelta(days=3)

    return super().save(*args,**kwargs)