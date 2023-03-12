from django.shortcuts import render
from django.http import HttpResponse
from .models import Listing
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'my_app/home.html')

def test(request):
    posts = Listing.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'my_app/test.html', context=context)
