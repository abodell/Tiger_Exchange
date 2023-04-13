from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.urls import reverse_lazy

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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    # believe total price would be a derived attribute so we wouldn't store it

class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length = 40)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    zip = models.CharField(max_length = 10)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

class OrderHistory(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['order_id', 'user_id'], name = "unique order")
        ]

class Listing(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length= 1024, blank=False)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart, blank=True)
    watchlist = models.ManyToManyField(WatchList, blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.title + " | " + str(self.author)

    def get_absolute_url(self):
        return reverse_lazy('my_app:detail_list', args=(str(self.id)))

@receiver(post_delete, sender=Listing)
def delete_image_on_listing_delete(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image.path)
    
class OrderProducts(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Listing, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['order_id', 'product_id'], name = 'unique order item')
        ]