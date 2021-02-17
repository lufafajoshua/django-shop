from django.db import models
from user_profiles.models import User
from django.conf import settings


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    #You can include othe rspecific data to the seller. for example image data  

    def __str__(self):
        return self.user.username