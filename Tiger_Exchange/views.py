from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from .forms import CreateUserForm
from django.contrib.auth.models import User
from my_app.models import Profile
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
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context=context)

def cart(request):
    return render(request,'my_app/cart.html')

def useraccount(request):
    current_user = request.user
    profile = User.objects.all().filter(username = current_user)
    context = {
        'profile': profile[0]
    }
    return render(request,'my_app/user_account.html', context=context)