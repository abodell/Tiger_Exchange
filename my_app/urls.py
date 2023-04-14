from django.urls import path 
from . import views 

app_name = 'my_app'

urlpatterns = [
    path('', views.home,name='home'),
    # path('test_list_view', views.testListView.as_view(), name='list'),
    # path('test_listings/<int:pk>', views.TestDetailView.as_view(), name='detail_list'),
    path('create_listing/', views.createListingView, name='create_listing'),
    path('my_listings/', views.myListingsView, name='my_listings'),
    path('listings/<int:id>/<str:type>', views.listingDetailView, name='listing_detail'),
    path('create_chat/<int:seller_pk>/', views.create_chat, name='create_chat'),
    
    path('dev/seed-data/', views.seedData, name='seed_data'),
    path('dev/create-accounts/', views.createAccounts, name='create_test_accounts'),
    path('dev/delete-all-listings', views.deleteAllListings, name='delete_all_listings'),
    path('dev/delete-listing/<int:id>', views.deleteListing, name='delete_listing')
]