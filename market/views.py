# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from market.models import UserProfile
from django.http import HttpResponse

# Create your views here.
def users(request):
    user_list = UserProfile.objects.all()[:5]
    context_dict = {'users' : user_list }
    
    return render(request, 'market/users.html', context_dict)
    
def index(request):
    
    return render(request, 'market/index.html', {})