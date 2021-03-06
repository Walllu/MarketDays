# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import User
from django.db.models import F
from market.models import UserProfile, Item, Session, Offer, SessionParticipants, OfferContent
from django.contrib.auth.decorators import login_required
from market.forms import UserForm, UserProfileForm, ItemForm
import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.db.models import Max
from django.http import JsonResponse
import json

# Create your views here.
################ helper methods #########################
# this method returns the UserProfile of whoever sent in the request
# to be called only in methods restricted to login_required
def get_current_user(req):
    user = req.user # this is the User instance
    return UserProfile.objects.get(user=user) # this is the UserProfile instance, return to caller

# this method finds all offers involving the item
# to be called when an offer transacting these items is accepted, effectively deleting offers that are now null
def delete_all_offers_containing(item): # accepts an Item object
    assoc_offerIDs = OfferContent.objects.filter(itemID=item) # get all the offerIDs involving the item in questio
    for ID in assoc_offerIDs: # delete every offer, cascading down to offer contents as well
        print(str(ID.offerID) + " to be deleted")
        try:
            offer = Offer.objects.get(offerID__exact=ID.offerID.offerID)
            offer.delete()
            print("item deleted")
        except Offer.DoesNotExist:
            print("not deleted, already does not exist")
            continue # the point is we're trying to delete these things, if it doesn't exist already then less work for us!

########################################################3
# returns the about page
def about(request):
    return render(request, 'market/about.html', {})

#view for handling logging in
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
            print(("Invalid login details: {0}, {1}".format(username, password)))
            return HttpResponse("Invalid login details supplied.")
    # request is not a HTTP POST so display the login form
    # this scenario will most likely be a HTTP GET
    else:
        #No context variables hence the empty dictionary
        return render(request, 'market/login.html', {})


#view that handles registering
def register(request):
    # a boolean to keep track of whether or not registration worked
    registered = False
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)

        #if the two forms are valid
        if profile_form.is_valid():
            print("hello")
            profile = profile_form.save(commit=False)
            profile.password = make_password(profile.password)

            id = UserProfile.objects.all().aggregate(Max('userID'))
            num = id['userID__max']

            profile.userID = num + 1
            profile.userStartDate = datetime.date.today()

            profile.save()
            registered = True
        else:
            #invalid form or forms
            print((profile_form.errors))
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input
        # user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'profile_form': profile_form, 'registered': registered}
    return render(request, 'market/register.html', context)


# could we please change this view to do something meaningful? should probably present user login here yeah?
def index(request):
    context_dict = {'boldmessage': "index view demo"}
    return render(request, 'market/index.html', context = context_dict)


# This view function should request a user's profile from the databases
# one does not need to be logged in to view this, though if you are, you should be able to a list of items
# Walter - 10.3.18


# This one is for VIEWING user profiles
def view_user(request, user_name_slug=None):
    context_dict = {}
    try: # try to find the user in the db
        userprof = UserProfile.objects.get(slug=user_name_slug.lower())
        context_dict['userprofile_object'] = userprof
    except UserProfile.DoesNotExist:
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
    current_user = get_current_user(request)
    session_to_join = Session.objects.get(slug__exact=session_slug)
    if not session_slug:
        return HttpResponseRedirect(reverse('sessionlist'))

    #check to see if user is already a part of a market session
    if SessionParticipants.objects.filter(sessionID=session_to_join, participantID=current_user).exists():
        # if the user is part of the market session in question
        return HttpResponseRedirect(reverse('view_market', kwargs={'session_slug':session_slug}))
    elif SessionParticipants.objects.filter(participantID=current_user).exists():
        # if the user is part of a market session, but not this one
        return HttpResponseRedirect(reverse('sessionlist'))
    else:
        if request.method == "GET":
            # increment Session participants attribute
            session_to_join.participants = F('participants') + 1
            session_to_join.save()
            # add SessionParticipant
            session_participant_info = SessionParticipants(sessionID=session_to_join, participantID=current_user)
            session_participant_info.save()

            return HttpResponseRedirect(reverse('view_market', kwargs={'session_slug':session_slug}))
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
            print((item_form.errors))
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
        # check if current user is part of the session
        current_user = get_current_user(request)
        context_dict['current_user_object'] = current_user
        if not SessionParticipants.objects.filter(sessionID=session, participantID=current_user).exists():
            print("This user is not part of this session - YOU SHALL NOT PASS!!!")
            return HttpResponseRedirect(reverse('sessionlist'))
    except Session.DoesNotExist:
        context_dict['session_object'] = None
    # get users in the session
    try:
        session = context_dict['session_object']
        if (not session==None) and (session.participants>0): # if session exists and it has more than 0 participants, then find all users within session
            # if session exists with more than 0 participants, then it is assumed that at least one SessionParticipants object exists
            users_in_session = SessionParticipants.objects.filter(sessionID__exact=session.sessionID)

            context_dict['users_in_session'] = users_in_session
        else:
            context_dict['users_in_session'] = None
    except SessionParticipants.DoesNotExist: # if there is an error for some reason, make None
        print("there are no users in this session")
        context_dict['users_in_session'] = None


    return render(request, 'market/show_session.html', context_dict)


@login_required
def begin_haggle(request, item_id=None):
    context_dict = {}
    # open a new haggle view for the item of "item_id"
    # make an OfferForm?
    # get the current user's items
    current_user = get_current_user(request)
    context_dict['current_user_object'] = current_user
    itemcount = Item.objects.filter(claimantID__exact=current_user).count()
    if itemcount == 0:
        context_dict['current_user_item_count'] = None
    else:
        context_dict['current_user_item_count'] = True
    # get opposing user's items
    item_in_question = Item.objects.get(itemID__exact=item_id)
    context_dict['item_in_question'] = item_in_question
    opponent = UserProfile.objects.get(userID__exact=item_in_question.claimantID.userID)
    context_dict['opponent'] = opponent
    return render(request, 'market/haggle.html', context_dict)


#view for creating user profile after creating a user (second step in django registration redux)
@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            id = UserProfile.objects.all().aggregate(Max('userID'))
            num = id['userID__max']
            try: #if empty database
                user_profile.userID = num + 1
            except:
                user_profile.userID =  1
            user_profile.save()


            return redirect('/market/')
        else:
            print((form.errors))

    context_dict = {'form' : form}

    return render(request, 'market/profile_registration.html', context_dict)


# this view is meant for a USER TO EDIT HIS/HER OWN DETAILS
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'firstName' : userprofile.firstName, 'lastName': userprofile.lastName})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'market/userProfile.html', {'userprofile_object':userprofile,'selecteduser':user,'form':form})


#adding items
@login_required
def add_item(request, username):
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            user = User.objects.get(username=username)
            user = UserProfile.objects.get(user=user)
            print(user.userID)
            item.possessorID = user
            item.claimantID = item.possessorID

            try: #if empty database
                id = Item.objects.all().aggregate(Max('itemID'))
                num = id['itemID__max']
                item.itemID = num + 1
            except:
                item.itemID =  1

            item.save()


            return HttpResponseRedirect(reverse('view_user', kwargs={'user_name_slug':user.slug}))
        else:
            print(form.errors)

    context_dict = {'form' : form}

    return render(request, 'market/add_item.html', context_dict)


#view for displaying offers user is involved in
@login_required
def show_notifications(request, username):
    context_dict={}
    try: # try to find the user in the db
        user = User.objects.get(username=username)
        userprof = UserProfile.objects.get(user=user)
        context_dict['userprofile_object'] = userprof
    except UserProfile.DoesNotExist:
        context_dict['userprofile_object'] = None
    return render(request, 'market/show_notifications.html', context = context_dict)


@login_required
def makeoffer(request):
    if request.method == 'POST':
        #now we want to go ahead and make a new Offer
        unicode_body = json.loads(request.body.decode('utf-8')) # get the contents of the AJAX post
        current_user = get_current_user(request)
        LHS = unicode_body['LHS']
        RHS = unicode_body['RHS']
        message = unicode_body['message']
        opponentID = unicode_body['opponent_ID']
        opponent = UserProfile.objects.get(userID__exact=opponentID)
        # make new offer with this information
        ID = Offer.objects.all().aggregate(Max('offerID')) # this returns a list of offerIDs
        maxID = ID['offerID__max']
        try:
            offer = Offer(offerID=maxID+1, fromID=current_user, toID=opponent, message=message)
        except:
            offer = Offer(offerID=0, fromID=current_user, toID=opponent, message=message)
        offer.save()
        # populate offer contents
        for fromItem in LHS:
            fromItem = int(fromItem)
            thisitem = Item.objects.get(itemID__exact=fromItem)
            content = OfferContent(callerID=current_user, calleeID=opponent, itemID=thisitem, offerID=offer)
            content.save()
        for toItem in RHS:
            toItem = int(toItem)
            thisitem = Item.objects.get(itemID__exact=toItem)
            content = OfferContent(callerID=current_user, calleeID=opponent, itemID=thisitem, offerID=offer, offered=False)
            content.save()

        return JsonResponse({})
    else:
        return None


# this method allows an item to be deleted
# should only be possible if the current user owns physially and by claim
@login_required
def delete_item(request, itemID):
    current_user = get_current_user(request)
    item = Item.objects.get(itemID__exact=int(itemID))
    if item.possessorID.slug == item.claimantID.slug:
        Item.objects.filter(itemID__exact=itemID).delete()
        return redirect('/market/viewuser/'+item.possessorID.slug)
    else:
        return redirect('/market/viewuser/'+item.possessorID.slug)
        #we need to add a message that would say that you cannot delete not yours item


@login_required
def delete_offer(request, offerID):
    offer = Offer.objects.get(offerID__exact=int(offerID))
    Offer.objects.filter(offerID__exact=offerID).delete()
    try:
        return redirect('/market/notifications/'+offer.fromID.user.username)
    except:
        return redirect('/market/notifications/'+offer.toID.user.username)


@login_required
def counter_offer(request, offerID):
    # this view should render the counter offer template
    context_dict = {}
    current_user = get_current_user(request)
    context_dict['userID'] = current_user.userID
    try:
        offer = Offer.objects.get(offerID__exact=offerID)
        current_user = offer.toID
        opponent = offer.fromID
        context_dict['offer_object'] = offer
        context_dict['opponent'] = opponent
        context_dict['current_user_object'] = current_user
    except Offer.DoesNotExist:
        context_dict['opponent'] = None
        context_dict['offer_object'] = None
        context_dict['current_user_object'] = None

    #include current user details
    itemcount = Item.objects.filter(claimantID__exact=current_user).count()
    if itemcount == 0:
        context_dict['current_user_item_count'] = None
    else:
        context_dict['current_user_item_count'] = True

    return render(request, 'market/counteroffer.html', context_dict)


@login_required
def accept_offer(request):
    if request.method == 'POST':
        # here we want to check if accept_offer is true
        unicode_body = json.loads(request.body.decode('utf-8')) # get the contents of the AJAX post
        accept = unicode_body['accept_offer']
        offerID = unicode_body['offer_ID']
        if accept:
            try:
                offer = Offer.objects.get(offerID__exact=offerID)
                yourID = offer.toID
                oppID = offer.fromID
                # get the items from the offer
                youGetID = OfferContent.objects.filter(offerID__exact=offer).exclude(offered=True).values('itemID')
                youGiveID = OfferContent.objects.filter(offerID__exact=offer).exclude(offered=False).values('itemID')
                # for each item in youGetID/youGiveID, change claimantID to be the other
                # and delete all offers containing these items - a process which gets faster with each item (or should)
                youGetItems = [Item.objects.get(itemID__exact=ID['itemID']) for ID in youGetID] # list of items you get
                youGiveItems = [Item.objects.get(itemID__exact=ID['itemID']) for ID in youGiveID]
                for item in youGetItems:
                    item.claimantID = oppID
                    item.save()
                    delete_all_offers_containing(item) # delete all the offers associated with this item
                for item in youGiveItems:
                    item.claimantID = yourID
                    item.save()
                    delete_all_offers_containing(item) # delete all offers associated with this item
                return JsonResponse({})
            except Offer.DoesNotExist:
                # the offer does not exist, so redirect to current_user's notifications page
                return HttpResponseRedirect(reverse('notifications', current_user.userID))


#when session is done user can let the app now that he got physically his item
@login_required
def collect_item(request, itemID):
    item = Item.objects.get(itemID__exact=int(itemID))
    item.possessorID = item.claimantID # change physical ownership of an item
    item.save()
    context_dict = {}
    userprof = item.possessorID
    context_dict['userprofile_object'] = userprof

    #return HttpResponse("Hope you gonna enjoy your new item just like you do MarketDays :P")
    return render(request, 'market/viewuser.html', context_dict)
