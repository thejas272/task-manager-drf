from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TaskModel(models.Model):
  owner = models.ForeignKey(User,on_delete=models.CASCADE, null=False, blank=False)

  title       = models.CharField(max_length=300,null=False, blank=False)
  description = models.TextField(null=True, blank=True)
  status      = models.BooleanField(default=False)

  created_at  = models.DateTimeField(auto_now_add=True)
  updated_at  = models.DateTimeField(auto_now=True) 


  def __str__(self):
    return f"task - '{self.title}' of user - '{self.owner.username}'"
  