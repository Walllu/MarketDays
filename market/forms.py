from django import forms
from django.contrib.auth.models import User
from market.models import UserProfile, Item, Offer
import datetime

from django.core.validators import RegexValidator

# this is for user registration
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # this entire class comes straight outta rango
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

#this is used at the account edit stage, when you've logged in and edit your account
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstName','lastName','userPhoneNumber','userDescription','userInterests', 'picture')

#this for is used when adding items
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('itemName', 'itemDescription', 'picture')

'''
class OfferForm(forms.ModelForm):
    pass
'''
