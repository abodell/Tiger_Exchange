from django.contrib import admin
from .models import Listing, Category, Cart, Profile

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Profile)