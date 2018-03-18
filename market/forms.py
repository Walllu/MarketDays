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
    #password = forms.CharField(widget=forms.PasswordInput())
    #userName = forms.CharField(max_length=15, help_text="first name")
    #firstName = forms.CharField(max_length=20, help_text="first name")
    #lastName = forms.CharField(max_length=20, help_text="last name")
    # I pulled the phonenumber line from StackOverflow
    #userPhoneNumber = forms.CharField(max_length=15)
    #userDescription = forms.CharField(max_length=512, help_text="Please enter description...")
    #userInterests = forms.CharField(max_length=512, help_text="What are you interested in?")
    #userStartDate = forms.CharField(max_length=15)#models.DateField(_("Date"), default=datetime.date.today) to be sorted later
    class Meta:
        model = UserProfile
        #exclude = ('userName','password')#'userName','email','password'
        fields = ('firstName','lastName','userPhoneNumber','userDescription','userInterests', 'picture')

class ItemForm(forms.ModelForm):
    print "lol"
    # itemID = Get next ID
    # possessorID = get user ID
    # claimantID = get user ID
    # itemName = set by user
    # itemDescription = set by user
    # itemDatePosted = get date
    # slug = itemName + itemID
    class Meta:
        model = Item
        fields = ('itemName', 'itemDescription', 'picture')

class OfferForm(forms.ModelForm):
    pass
