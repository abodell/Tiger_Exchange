from django.db import models

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