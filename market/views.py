# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from market.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def users(request):
    user_list = UserProfile.objects.all()[:5]
    context_dict = {'users' : user_list }

    return render(request, 'market/users.html', context_dict)

def userProfile(request):
    context_dict = {}

    return render(request, 'market/userProfile.html', context_dict)


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
