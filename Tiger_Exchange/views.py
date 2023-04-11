from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from my_app.models import Profile, Cart, Listing
from django.contrib import messages
from django.urls import reverse_lazy

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
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context=context)

@login_required
def cart(request):
    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    if not profile:
        return render(request, 'registration/signup.html')
    userID = profile[0].pk
    cart = Cart.objects.filter(user_id = userID)
    cartListings = Listing.objects.all().filter(cart = cart[0])
    if len(cartListings) > 0:
        context = {
        'listings': cartListings
        }
    else:
        context = {
            'message': "You have nothing in your cart!"
        }
    return render(request,'my_app/cart.html', context=context)


def useraccount(request):
    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    if not profile:
        return render(request, 'registration/signup.html')
    context = {
        'profile': profile[0]
    }
    return render(request,'my_app/user_account.html', context=context)