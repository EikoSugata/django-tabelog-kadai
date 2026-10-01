from django.db import models
import os
from .category import Category

def upload_image_to(instance, filename):
  restaurant_id = instance.id
  return os.path.join('static', 'restaurants', restaurant_id, filename)

class Restaurant(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)
  image = models.ImageField(blank=True, upload_to=upload_image_to)
  description = models.TextField(blank=True)
  open_time = models.TimeField()
  close_time = models.TimeField()
  postal_code = models.CharField(max_length=8)
  address = models.TextField()
  phone_number = models.CharField(max_length=15)
  is_published = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.name