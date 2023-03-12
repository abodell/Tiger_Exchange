# from django import forms
# from .models import Listing

# class ListingForm(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = ('title', 'description', 'price', 'author')

#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'price': forms.FloatField(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-control'})
#         }