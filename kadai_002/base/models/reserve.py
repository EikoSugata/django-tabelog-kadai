from django.db import models
from .restaurant import Restaurant
from .user import User

class Reserve(models.Model):
  id = models.AutoField(primary_key=True)  
  reserve_at = models.DateTimeField()
  people_num = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  restaurant_id = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
  user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return str(self.id)