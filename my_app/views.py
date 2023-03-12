from django.shortcuts import render
from django.http import HttpResponse
from .models import Listing
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import ListingForm
# Create your views here.

def home(request):
    return render(request,'my_app/home.html')

def test(request):
    posts = Listing.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'my_app/test.html', context=context)

class testListView(ListView):
    model = Listing
    template_name = 'my_app/test_list_view.html'

class TestDetailView(DetailView):
    model = Listing
    template_name = 'my_app/test_list_detail.html'


class createListingView(LoginRequiredMixin, CreateView):
    model = Listing
    template_name = 'my_app/create_listing.html'
    # form_class = ListingForm
    # fields = '__all__'
    fields = ('title', 'description', 'price', 'category', 'image')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)