from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from .forms import CreateUserForm
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

