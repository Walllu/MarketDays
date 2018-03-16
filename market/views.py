# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from models import User
from market.models import UserProfile, Item
from django.contrib.auth.decorators import login_required
from market.forms import UserForm, UserProfileForm, ItemForm
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.db.models import Max

# Create your views here.
def users(request):
    user_list = UserProfile.objects.all()[:5]
    context_dict = {'users' : user_list }

    return render(request, 'market/users.html', context_dict)


# added this to pass a test I wrote - up to someone else whether we keep it or not
def about(request):
    pass

def user_login(request):
    if request.method == 'POST':
        # use request.Post.get('<variable>') instead of request.POST['<variable>'] because the first returns
        # None if the value doesn't exist, and the latter method returns a KeyError exception in the same situation
        username = request.POST.get('username')
        password = request.POST.get('password')
        #passwordhash = make_password(password)


        user = authenticate(username=username, password=password)
        if user:
            # is the account enabled or disabled?
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # account is inactive, so no logging in for youu
                return HttpResponse("Your MarketDays account is disabled")
        else:
            # Bad login details were provided
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # request is not a HTTP POST so display the login form
    # this scenario will most likely be a HTTP GET
    else:
        #No context variables hence the empty dictionary
        return render(request, 'market/login.html', {})

def register(request):
    # a boolean to keep track of whether or not registration worked
    print "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
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
            #profile.password = make_password(profile.password)
            profile.password = make_password(profile.password)

            id = UserProfile.objects.all().aggregate(Max('userID'))
            num = id['userID__max']

            profile.userID = num + 1
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


# This view function should request a user's profile from the databases
# one does not need to be logged in to view this, though if you are, you should be able to a list of items
# Walter - 10.3.18


# This one is for VIEWING
def view_user(request, user_name_slug=None):
    context_dict = {}
    try: # try to find the user in the db
        print "lol"
        userprof = UserProfile.objects.get(slug=user_name_slug)
        print "after user"
        context_dict['userprofile_object'] = userprof
    except UserProfile.DoesNotExist:
        print "lol2"
        context_dict['userprofile_object'] = None
    # context dictionary for the userProfile template now contains information regarding the user to whom it belongs
    return render(request, 'market/viewuser.html', context_dict)



# --------------------------- the following views require user to be logged in -------------------- #


# this view shows the session list
@login_required
def sessionlist(request):
    context_dict = {}
    return render(request, 'market/sessionlist.html', context_dict)

@login_required
def join_session(request, session_slug=None):
    # if there's a slug parameter, then we want to add SessionParticipant, and increment participants in Session, and redirect to home
    # should check if you are already part of a session - if so, do not procede
    if not session_slug:
        return HttpResponseRedirect(reverse('sessionlist'))
    else:
        if request.method == "GET":
            # increment Session participants attribute
            # add SessionParticipant
            pass
        else:
            return HttpResponseRedirect(reverse('sessionlist'))



@login_required
def register_item(request, username):
    # a boolean to keep track of whether or not registration worked
    registered = False
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        item_form = ItemForm(data=request.POST)

        #if the two forms are valid
        if item_form.is_valid():
            print "hello"

            user = UserProfile.objects.get(userName=username)
            item = item_form.save(commit=False)
            item.possessorID = user['userID']
            item.claimantID = item.possessorID

            

            id = Item.objects.all().aggregate(Max('itemID'))
            num = id['itemID__max']

            item.itemID = id + 1
            #profile.user = user
            item.itemDatePosted = datetime.date.today()

            item.save()
            registered = True
        else:
            #invalid form or forms
            print(item_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input
        # user_form = UserForm()
        item_form = ItemForm()
    context = {'item_form': item_form, 'registered': registered}
    return render(request, 'market/register_item.html', context)

#this view shows the list of 
@login_required
def show_market_session(request, session_slug=None):
    context_dict = {}
    # get the session
    try:
        session = Session.objects.get(slug=session_slug)
        context_dict['session_object'] = session
    except Session.DoesNotExist:
        context_dict['session_object'] = None
    # get users in the session
    try:
        session = context_dict['session_object']
        if (not session==None) and (session.participants>0): # if session exists and it has more than 0 participants, then find all users within session
            # if session exists with more than 0 participants, then it is assumed that at least one SessionParticipants object exists
            users_in_session = SessionParticipants.objects.get(sessionID__exact=session.sessionID)
            context_dict['users_in_session'] = users_in_session
        else:
            context_dict['users_in_session'] = None
    except SessionParticipants.DoesNotExist: # if there is an error for some reason, make None
        context_dict['users_in_session'] = None

    return render(request, 'market/show_session.html', context_dict)

@login_required
def restricted(request):
    return HttpResponse("thx for logging in")

@login_required
def register_profile(request):
    print "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            id = UserProfile.objects.all().aggregate(Max('userID'))
            num = id['userID__max']
            user_profile.userID = num + 1
            user_profile.save()


            return redirect('/market/')
        else:
            print (form.errors)

    context_dict = {'form' : form}

    return render(request, 'market/profile_registration.html', context_dict)


# this view is meant for a USER TO EDIT HIS/HER OWN DETAILS
@login_required
def profile(request, username):
    print "llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'userName' : userprofile.firstName, 'lastname': userprofile.lastName})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print form.errors

    return render(request, 'market/userProfile.html', {'userprofile':userprofile,'selecteduser':user,'form':form})
