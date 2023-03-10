from django.urls import path 
from . import views 

app_name = 'my_app'

urlpatterns = [
    path('', views.home,name='home'),
    path('test/', views.test, name='test'),
    path('test_list_view', views.testListView.as_view(), name='list'),
    path('test_listings/<int:pk>', views.TestDetailView.as_view(), name='detail_list'),
    path('create_listing/', views.createListingView.as_view(), name='create_listing')
]