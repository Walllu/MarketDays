# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from market.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from market.forms import UserForm, UserProfileForm
import datetime
from django.contrib.auth.hashers import make_password

# Create your views here.
def users(request):
    user_list = UserProfile.objects.all()[:5]
    context_dict = {'users' : user_list }

    return render(request, 'market/users.html', context_dict)

def userProfile(request):
    context_dict = {}

    return render(request, 'market/userProfile.html', context_dict)
    
def register(request):
    # a boolean to keep track of whether or not registration worked
    registered = False
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if the two forms are valid
        if profile_form.is_valid():
            print "hello"
            # user = user_form.save()
            #hash the password with set_password method
            
            # user.save()

            profile = profile_form.save(commit=False)
            profile.password = make_password(profile.password)
            #profile.user = user
            profile.userStartDate = datetime.date.today()

            profile.save()
            registered = True
        else:
            #invalid form or forms
            print(profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input
        # user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'profile_form': profile_form, 'registered': registered}
    return render(request, 'market/register.html', context)


# I added these two in order to pass the tests I wrote -Walter 9.3.18
def sessionlist(request):
    pass

def about(request):
    pass


# could we please change this view to do something meaningful? should probably present user login here yeah?
def index(request):
    #request.session.set_test_cookie()
    #category_list = Category.objects.order_by('-likes')[:5]
    #pages_list = Page.objects.order_by('-views')[:5]
    #context_dict = {}#{'categories': category_list, 'pages': pages_list}


    #visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    context_dict = {'boldmessage': "yoyoyo"}
    return render(request, 'market/index.html', context = context_dict)

@login_required
def restricted(request):
    return HttpResponse("thx for logging in")
