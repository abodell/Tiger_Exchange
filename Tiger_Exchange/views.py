from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from my_app.models import Profile, Cart, Listing, WatchList
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator

def SignupView(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            newUser = User.objects.get(username = user)
            cart = Cart(user_id = newUser, quantity = 0)
            cart.save()
            watchlist = WatchList(user_id = newUser)
            watchlist.save()
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context=context)

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user)
    cartListings = Listing.objects.filter(cart=cart)
    # current_user = request.user
    # profile = User.objects.all().filter(username = current_user)
    # if not profile:
    #     return render(request, 'registration/signup.html')
    # userID = profile[0].pk
    # cart = Cart.objects.filter(user_id = userID)
    # cartListings = Listing.objects.all().filter(cart = cart[0])

    # If a search query is submitted, filter the queryset by name
    search_query = request.GET.get('q')
    if search_query:
        cartListings = cartListings.filter(title__icontains=search_query)

    # If a filter value is submitted, filter the queryset by category
    filter_value = request.GET.get('category')
    if filter_value and filter_value != 'all':
        cartListings = cartListings.filter(category=filter_value)

    cartListings = cartListings.order_by('title')

    paginator = Paginator(cartListings, 50)
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


    if len(cartListings) > 0:
        context = {
            'listings': cartListings,
            'page_obj': page_obj,
            'num_pages': paginator.num_pages,
            'page_range': page_range,
            'search': search_query,
            'category': filter_value,
        }
    else:
        context = {
            'message': "You have nothing in your cart!"
        }
    return render(request,'my_app/cart.html', context=context)

@login_required
def watchlist(request):
    watchlist, created = WatchList.objects.get_or_create(user_id=request.user)
    watchlistListings = watchlist.listing_set.all()

    # current_user = request.user
    # profile = User.objects.all().filter(username = current_user)
    # if not profile:
    #     return render(request, 'registration/signup.html')
    # userID = profile[0].pk
    # watchlist = WatchList.objects.filter(user_id = userID)
    # watchlistListings = Listing.objects.all().filter(watchlist = watchlist[0])

    # If a search query is submitted, filter the queryset by name
    search_query = request.GET.get('q')
    if search_query:
        watchlistListings = watchlistListings.filter(title__icontains=search_query)

    # If a filter value is submitted, filter the queryset by category
    filter_value = request.GET.get('category')
    if filter_value and filter_value != 'all':
        watchlistListings = watchlistListings.filter(category=filter_value)

    watchlistListings = watchlistListings.order_by('title')

    paginator = Paginator(watchlistListings, 50)
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

    if len(watchlistListings) > 0:
        context = {
            'num_pages': paginator.num_pages,
            'listings': watchlistListings,
            'page_obj': page_obj,
            'page_range': page_range,
            'search': search_query,
            'category': filter_value,
        }
    else:
        context = {
            'message': "You have nothing on your watchlist!"
        }
    return render(request, 'my_app/watchlist.html', context=context)

@login_required
def useraccount(request):
    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    if not profile:
        return render(request, 'registration/signup.html')
    context = {
        'profile': profile[0]
    }
    return render(request,'my_app/user_account.html', context=context)