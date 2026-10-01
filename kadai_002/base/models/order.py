from django.db import models
from django.contrib.auth import get_user_model

class Order(models.Model):
  id = models.AutoField(primary_key=True)
  amount = models.PositiveIntegerField(default=0)
  is_confirmed = models.BooleanField(default=False)
  subscription_start_at=models.DateTimeField()
  subscription_end_at=models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

  def __str__(self):
    return str(self.created_at)