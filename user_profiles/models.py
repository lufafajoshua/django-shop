from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _


#Product = apps.get_model('products.Product')

class User(AbstractUser):
  #email = models.EmailField(_('email address'), unique=True) 
  USER_TYPE_CHOICES = (
      (1, 'customer'),
      (2, 'seller'),
      (3, 'agent'),
      (4, 'admin'),
  )

  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
  REQUIRED_FIELDS = ['user_type', 'email']

  objects = CustomUserManager()


class Profile(models.Model):#This is the profile of the customer that will be tied to their orders
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ebooks = models.ManyToManyField('products.Product', blank=True)#These are the products purcased byt eh customer

    def __str__(self):
        return self.user.username

    # class Agent(models.Model):
    #     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #     availability = models.BooleanField(default=True)
    #     email = models.EmailField(_('email address')) 

    #     def __str__(self):
    #         return self.user.username


"""Consider adding the admin to be created in the frontend"""
        # class Admin(models.Model):
        #     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        #     #username = None
        #     email = models.EmailField(_('email address'), unique=True)

class UserAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
