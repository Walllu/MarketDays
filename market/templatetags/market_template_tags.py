from django import template
from market.models import UserProfile, Session, Offer, Item, SessionParticipants, OfferContent
import datetime, pytz


#Walter 26.2.2018
# This is just something here in case we want to use templatetags later on

register = template.Library()

# this is for the sessions list template
@register.inclusion_tag('market/sesh.html')
def get_session_list():
    return {'sessions': Session.objects.all()}

# these methods will be used to render areas of the site with a certain list of
# tradable items, called depending on context
@register.inclusion_tag('market/items.html')
def get_your_items(yourID):  #this method should return all tradable and nontradable Items
    #next 5 lines are there to figure out if the session already expired, because if so then users can start colleting their items
    context_dict = {'yourtradable': Item.objects.filter(claimantID__exact=yourID),'yournontradable': Item.objects.filter(possessorID__exact=yourID).exclude(claimantID__exact=yourID),'yourID':yourID}
    try:
        sessionParticipant = SessionParticipants.objects.get(participantID=yourID)
        sessionEnd = sessionParticipant.sessionID.sessionEnd
        now = datetime.datetime.now()
        now = now.replace(tzinfo=pytz.UTC)
        sessionFinished = now > sessionEnd
        context_dict['sessionFinished'] = sessionFinished
    except SessionParticipants.DoesNotExist:
        context_dict['sessionFinished'] = None # this line indicates that session participant does not exist

    return context_dict


@register.inclusion_tag('market/offer_items.html')  # This method returns all tradable items of other user
def get_tradable_items(uID):
    return {'tradable': Item.objects.filter(claimantID__exact=uID)}


@register.inclusion_tag('market/offer_items.html')
def get_offer_LHS(offerID):
    # this should return the callee items based on offerID
    offer = Offer.objects.get(offerID__exact=offerID)
    LHS = OfferContent.objects.filter(offerID=offer).exclude(offered=False).values('itemID')
    items = []
    for id in LHS:
        realID = id['itemID']
        items.append(Item.objects.get(itemID__exact=realID))
    return {'LHSitems':items}


@register.inclusion_tag('market/offer_items.html')
def get_offer_RHS(offerID):
    # this should return the caller items based on offerID
    offer = Offer.objects.get(offerID__exact=offerID)
    RHS = OfferContent.objects.filter(offerID=offer).exclude(offered=True).values('itemID')
    items = []
    for id in RHS:
        realID = id['itemID']
        items.append(Item.objects.get(itemID__exact=realID))
    return {'RHSitems':items}


@register.inclusion_tag('market/offer_items.html')
def get_tradable_exclude_LHS(offerID):
    # this should return a list of items tradeable by callee, but exclude those already on offer
    offer = Offer.objects.get(offerID__exact=offerID)
    callee = offer.toID
    tradable = Item.objects.filter(claimantID__exact=callee)
    tradableitems = [item for item in tradable]
    LHS = OfferContent.objects.filter(offerID=offer).exclude(offered=True).values('itemID')
    LHSitems = [Item.objects.get(itemID__exact=item['itemID']) for item in LHS]
    items = []
    for id in LHS:
        realID = id['itemID']
        items.append(Item.objects.get(itemID__exact=realID))
    # keep items in tradable but not in items
    tradable_exclude_LHS = []
    for item in tradable:
        if item in LHSitems:
            continue
        else:
            tradable_exclude_LHS.append(item)
    return {'LHSitems_sans':tradable_exclude_LHS}


@register.inclusion_tag('market/offer_items.html')
def get_tradable_exclude_RHS(offerID):
    # this should return a list of items tradeable by callee, but exclude those already on offer
    offer = Offer.objects.get(offerID__exact=offerID)
    caller = offer.fromID
    tradable = Item.objects.filter(claimantID__exact=caller)
    tradableitems = [item for item in tradable]
    RHS = OfferContent.objects.filter(offerID=offer).exclude(offered=False).values('itemID')
    RHSitems = [Item.objects.get(itemID__exact=item['itemID']) for item in RHS]
    items = []
    for id in RHS:
        realID = id['itemID']
        items.append(Item.objects.get(itemID__exact=realID))
    # keep items in tradable but not in items
    tradable_exclude_RHS = []
    for item in tradableitems:
        if item in RHSitems:
            continue
        else:
            tradable_exclude_RHS.append(item)
    return {'RHSitems_sans':tradable_exclude_RHS}


# this one is for when you're in a session - it produces the list of all items in session
@register.inclusion_tag('market/items.html')
def get_all_items(sessionID):
    session = Session.objects.get(sessionID=sessionID)
    # this method should return all items that are in a session
    # essentially all the items that are in the inventories of the user within a session
    session_participants = SessionParticipants.objects.filter(sessionID=session).values('participantID')     # get the userID of all participants - store as a QuerySet
    print(session_participants)
    session_items = [] # this list will contain Item objects
    if len(session_participants)==0: # quick check to see if there's any participants to begin with
        return {'sessionitems':None}
    else: # some participants exist
        for u in session_participants:
            uid = u['participantID'] # ID of user
            uitems = Item.objects.filter(possessorID=uid) # a QuerySet containing Item objects
            for item in uitems:
                session_items.append(item)
    return {'sessionitems': session_items}
    # NOTE: I think it should be fine passing a list - the important thing is that it's an iterable


#this to template tags below are to get all the offers user is involved in
#the one right beleow is returning offers user has made
@register.inclusion_tag('market/offer_snip.html')
def get_your_offers(yourID):
    allOffers = list(Offer.objects.filter(fromID__exact=yourID).values('offerID').values())
    allOffersParsed = []
    for offer in allOffers:
        recieverID = offer['toID_id']
        reciever = UserProfile.objects.get(userID__exact=int(recieverID))
        offer['toID_id']=reciever.user.username
        allOffersParsed += [offer]
    return {'yourOffers':allOffersParsed}


#the one below returns offers addresed to a user
@register.inclusion_tag('market/offer_snip.html')
def get_to_you_offers(yourID):
    allOffers = list(Offer.objects.filter(toID__exact=yourID).values('offerID').values())
    allOffersParsed = []
    for offer in allOffers:
        senderID = offer['fromID_id']
        sender = UserProfile.objects.get(userID__exact=int(senderID))
        offer['fromID_id']=sender.user.username
        allOffersParsed += [offer]
    return {'toYouOffers':allOffersParsed}
