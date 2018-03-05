from django import forms
from django.contrib.auth.models import User
from market.models import UserProfile, Item, Offer

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
    firstName = forms.CharField(max_length=20, help_text="first name")
    lastName = forms.CharField(max_length=20, help_text="last name")
    # I pulled the phonenumber line from StackOverflow
    userPhoneNumber = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    userDescription = forms.CharField(max_length=512, help_text="Please enter description...")
    userInterests = forms.CharField(max_length=512, help_text="What are you interested in?")
    userStartDate = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = UserProfile
        fields = ('firstName','lastName','userPhoneNumber','userDescription','userInterests')
