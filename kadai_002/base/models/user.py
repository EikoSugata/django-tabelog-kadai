from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager): 
  # 無料会員作成
  def create_user(self, username, password=None):
    user = self.model(
      username=username,    
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  # 管理者作成
  def create_superuser(self, username, password=None):
    user = self.create_user(
      username,
      password=password,
    )
    user.is_admin = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=50, unique=True)  
  name = models.CharField(max_length=50, blank=True)
  name_kana = models.CharField(max_length=50, blank=True) 
  phone_number=models.CharField(max_length=15, blank=True)
  email = models.EmailField(max_length=255, blank=True)
  is_subscriber=models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  stripe_id_subscription = models.CharField(max_length=255, blank=True)

  objects = UserManager()
  USERNAME_FIELD = 'username'
  EMAIL_FIELD = 'email'

  def __str__(self):
    return self.username

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True

  @property
  def is_staff(self):
    "Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
    return self.is_admin