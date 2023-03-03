from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

# Create your models here.

# add more later
class Post(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name