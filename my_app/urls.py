from django.urls import path 
from . import views 

app_name = 'my_app'

urlpatterns = [
    path('', views.home,name='home'),
]