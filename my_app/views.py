from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request,'my_app/home.html')

def test(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'my_app/test.html', context=context)
