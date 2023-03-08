from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
User._meta.get_field('email')._unique = True

# Create your models here.

# add more later
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length= 11, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    # believe total price would be a derived attribute so we wouldn't store it

class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length = 40)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    zip = models.CharField(max_length = 10)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

class OrderHistory(models.Model):
    order_id = models.ForeignKey(Orders, primary_key = True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['order_id', 'user_id'], name = "unique order")
        ]

class Product(models.Model):
    product_name = models.CharField(max_length=50, blank=False)
    product_desc = models.TextField(max_length= 200, blank=False)
    product_price = models.FloatField()
    image1 = models.FileField(blank=False)
    image2 = models.FileField(blank=False)
    image3 = models.FileField(blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class OrderProducts(models.Model):
    order_id = models.ForeignKey(Orders, primary_key = True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['order_id', 'product_id'], name = 'unique order item')
        ]