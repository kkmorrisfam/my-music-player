from django.db import models

# Create your models here.
""" 
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=120, blank=True)
    profile_description = models.TextField(max_length=500, blank=True)

   
    def __str__(self):
        return self.username or self.email
 """