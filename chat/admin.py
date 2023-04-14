from django.contrib import admin

from .models import Message, Chat, Contact
# Register your models here.

admin.site.register(Contact)
admin.site.register(Chat)
admin.site.register(Message)