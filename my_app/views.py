from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Listing, Category, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
# from .forms import ListingForm
# Create your views here.

def home(request):
    listings = Listing.objects.all()
    context = {
        'listings': listings
    }
    return render(request,'my_app/home.html', context=context)

class testListView(ListView):
    model = Listing
    template_name = 'my_app/test_list_view.html'

class TestDetailView(DetailView):
    model = Listing
    template_name = 'my_app/test_list_detail.html'

def cart(request):
    return render(request,'my_app/cart.html')




# class createListingView(LoginRequiredMixin, CreateView):
#     model = Listing
#     template_name = 'my_app/create_listing.html'
#     # form_class = ListingForm
#     # fields = '__all__'
#     fields = ('title', 'description', 'price', 'category', 'image')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    
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
