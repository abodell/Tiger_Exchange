from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Listing, Category, Profile, Cart, WatchList
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    queryset = Listing.objects.all()

    # If a search query is submitted, filter the queryset by name
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
    # If a filter value is submitted, filter the queryset by category
    filter_value = request.GET.get('category')
    if filter_value and filter_value != 'all':
        queryset = queryset.filter(category=filter_value)

    paginator = Paginator(queryset, 75)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'num_pages': paginator.num_pages,
        'search': search_query,
        'category': filter_value,
        'listings': queryset,
        'page_obj': page_obj,
    }
    return render(request,'my_app/home.html', context=context)

class testListView(ListView):
    model = Listing
    template_name = 'my_app/test_list_view.html'

class TestDetailView(DetailView):
    model = Listing
    template_name = 'my_app/test_list_detail.html'

@login_required    
def createListingView(request):
    if request.POST:
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('image')
        Listing.objects.create(title=title, description=description, price=price, category=category, image=image, author=request.user)
        
        messages.success(request, 'Listing created successfully.')

        return redirect(reverse('my_app:home'))
    
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    
    return render(request,'my_app/create_listing.html', context=context)

@login_required
def myListingsView(request):

    queryset = Listing.objects.filter(author=request.user)

    # If a search query is submitted, filter the queryset by name
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)

    # If a filter value is submitted, filter the queryset by category
    filter_value = request.GET.get('category')
    if filter_value and filter_value != 'all':
        queryset = queryset.filter(category=filter_value)

    paginator = Paginator(queryset, 75)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'num_pages': paginator.num_pages,
        'search': search_query,
        'category': filter_value,
        'listings': queryset,
        'page_obj': page_obj,
    }
    return render(request, 'my_app/my_listings.html', context=context)

def listingDetailView(request, id, type = 'None'):
    # will check request method then handle accordingly
    listing = Listing.objects.get(id=id)
    message = ""
    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    userID = profile[0].pk
    if request.POST:
        if type == 'cart':
            cart = Cart.objects.all().filter(user_id = userID)
            listing.cart.add(cart[0])
            message = "Item Added to Cart!"
        elif type == 'watchlist':
            watchlist = WatchList.objects.all().filter(user_id = userID)
            listing.watchlist.add(watchlist[0])
            message = 'Item Added to Your WatchList!'
    is_owner = listing.author == request.user
    context = {'listing': listing, 'is_owner': is_owner, 'message': message}
    return render(request, 'my_app/listing_detail.html', context=context)
