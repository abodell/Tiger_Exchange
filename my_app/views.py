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

    queryset = queryset.order_by('?')

    paginator = Paginator(queryset, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    page_range = paginator.page_range
    current_index = page_range.index(page_obj.number)
    max_index = len(page_range)
    start_index = max(current_index - 4, 0)
    end_index = min(max_index, start_index + 9)
    if end_index - start_index < 9:
        if start_index == 0:
            end_index = min(9, max_index)
        else:
            start_index = max(0, end_index - 9)
    page_range = page_range[start_index:end_index]


    context = {
        'num_pages': paginator.num_pages,
        'search': search_query,
        'category': filter_value,
        'listings': queryset,
        'page_obj': page_obj,
        'page_range': page_range
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

    queryset = queryset.order_by('title')

    paginator = Paginator(queryset, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    page_range = paginator.page_range
    current_index = page_range.index(page_obj.number)
    max_index = len(page_range)
    start_index = max(current_index - 4, 0)
    end_index = min(max_index, start_index + 9)
    if end_index - start_index < 9:
        if start_index == 0:
            end_index = min(9, max_index)
        else:
            start_index = max(0, end_index - 9)
    page_range = page_range[start_index:end_index]

    context = {
        'num_pages': paginator.num_pages,
        'search': search_query,
        'category': filter_value,
        'listings': queryset,
        'page_obj': page_obj,
        'page_range': page_range
    }
    return render(request, 'my_app/my_listings.html', context=context)

from django.contrib.auth.views import LoginView

def listingDetailView(request, id, type = 'None'):
    # will check request method then handle accordingly
    listing = Listing.objects.get(id=id)
    message = ""


    in_cart = False
    in_watchlist = False

    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    userID = profile[0].pk

    checkingCart = Cart.objects.all().filter(user_id = userID)
    try:
        checkListing = Listing.objects.get(cart = checkingCart[0], id = listing.pk)
        if checkListing.pk == listing.pk:
            in_cart = True
    except:
        print('not in cart')
    
    checkingWatchlist = WatchList.objects.all().filter(user_id = userID)
    try:
        checkInWatchList = Listing.objects.get(watchlist = checkingWatchlist[0], id = listing.pk)
        if checkInWatchList.pk == listing.pk:
            in_watchlist = True
    except:
        print('not in watchlist')


    if request.POST:
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next=/listings/{id}/detail')
        
        current_user = request.user
        profile = User.objects.all().filter(username = current_user)
        userID = profile[0].pk

        if type == 'cart':
            cart = Cart.objects.all().filter(user_id = userID)
            listing.cart.add(cart[0])
            message = "Item Added to Cart!"
        elif type == 'watchlist':
            watchlist = WatchList.objects.all().filter(user_id = userID)
           
            listing.watchlist.add(watchlist[0])
            message = 'Item Added to Your WatchList!'

        elif type == 'delete_cart':
            getCart = Cart.objects.all().filter(user_id = userID)
            listing.cart.remove(getCart[0])
            message = "Item Removed From Cart!"
            messages.success(request ,"Item Removed From Cart!")
            return redirect('/cart')
        elif type == 'delete_watchlist':
            getWatchList = WatchList.objects.all().filter(user_id = userID)
            listing.watchlist.remove(getWatchList[0])
            message = "Item Removed From Watchlist!"
            messages.success(request, "Item Removed From Watchlist!")
            return redirect('/watchlist')

    is_owner = listing.author == request.user
    context = {'listing': listing, 'is_owner': is_owner, 'message': message, 'in_cart': in_cart, 'in_watchlist': in_watchlist}
    return render(request, 'my_app/listing_detail.html', context=context)


import requests
import random
from django.core.files.base import ContentFile
import os
def seedData(request):
    categoryMap = {
        "smartphones": 7,
        "laptops": 11,
        "fragrances": 19,
        "skincare": 19,
        "groceries": 35,
        "home-decoration": 20,
        "furniture": 20,
        "tops": 8,
        "womens-dresses": 8,
        "womens-shoes": 8,
        "mens-shirts": 8,
        "mens-shoes": 8,
        "mens-watches": 21,
        "womens-watches": 21,
        "womens-bags": 8,
        "womens-jewellery": 21,
        "sunglasses": 8,
        "automotive": 16, 
        "motorcycle": 16,
        "lighting": 35
    }
    for _ in range(5):
        response = requests.get("https://dummyjson.com/products?limit=0")
        data = response.json()

        product = data['products'][0]
        for product in data['products']:
            title = product['title']
            description = product['description']
            price = product['price']
            category_text = product['category']
            category_id = categoryMap[category_text]
            category = Category.objects.get(id=category_id)
            random_user = random.choice(User.objects.all())

            listing = Listing(
                title=title,
                description=description,
                price=price,
                category=category,
                author=random_user,
            )
            listing.save()

            image_url = product['images'][0]
            response = requests.get(image_url)
            if response.status_code == 200:
                
                _, ext = os.path.splitext(image_url)
                ext = ext.lower()

                # Replace spaces with underscores and append the image extension
                image_name = f'{title.replace(" ", "_")}{ext}'
                listing.image.save(image_name, ContentFile(response.content), save=True)
            else:
                print(f"Failed to fetch image for listing {title}")

    return HttpResponse("Data seeding successful.")


def createAccounts(request):
    for i in range(100):
        username = f'user{i}'
        if User.objects.filter(username=username).exists():
            continue
        email = f'user{i}@gmail.com'
        if User.objects.filter(email=email).exists():
            continue
        password = "Password*"
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

    return HttpResponse("created users successfully")

def deleteAllListings(request):
    Listing.objects.all().delete()
    return HttpResponse("deleted all listings")

def deleteListing(request, id):
    Listing.objects.filter(id=id).delete()
    return HttpResponse(f'deleted listing id {id}')

def deleteAccounts(request):
    User.objects.all().delete()
    # User.objects.all().delete()
    return HttpResponse("deleted all accounts")



from chat.models import Contact, Chat

@login_required
def create_chat(request, seller_pk):
    # Get or create the current user's Contact object
    buyer_contact, created = Contact.objects.get_or_create(user=request.user)

    # Get or create the seller's Contact object
    seller_contact, created = Contact.objects.get_or_create(user_id=seller_pk)

    # Check if a chat room with these two participants already exists
    chat_room = Chat.objects.filter(participants=buyer_contact).filter(participants=seller_contact).first()

    if not chat_room:
        # Create a new chat room with the buyer and seller as participants
        chat_room = Chat.objects.create()
        chat_room.participants.add(buyer_contact, seller_contact)
        chat_room.save()

    # Redirect the user to the new chat room
    return redirect('chat:room', room_name=chat_room.pk)