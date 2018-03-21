from django import template
from market.models import UserProfile, Session, Offer, Item, SessionParticipants, OfferContent

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
    return {'yourtradable': Item.objects.filter(claimantID__exact=yourID), 'yournontradable': Item.objects.filter(possessorID__exact=yourID).exclude(claimantID__exact=yourID)}

@register.inclusion_tag('market/offer_items.html')  # This method returns all tradable items of other user
def get_tradable_items(uID):
    return {'tradable': Item.objects.filter(claimantID__exact=uID)}

"""
@register.inclusion_tag('market/items.html')
def get_items_by_ownership(userID):
    return {}
"""

# this one is for when you're in a session - it produces the list of all items in session
@register.inclusion_tag('market/items.html')
def get_all_items(sessionID):
    # this method should return all items that are in a session
    # essentially all the items that are in the inventories of the user within a session
    session_participants = SessionParticipants.objects.filter(sessionID__exact=sessionID).values('participantID')     # get the userID of all participants - store as a QuerySet
    print session_participants
    session_items = [] # this list will contain Item objects
    if len(session_participants)==0: # quick check to see if there's any participants to begin with
        return {'sessionitems':None}
    else: # some participants exist
        for u in session_participants:
            uid = u['participantID'] # ID of user
            uitems = Item.objects.filter(possessorID=uid) # a QuerySet containing Item objects
            for item in uitems:
                session_items.append(item)
    print session_items
    return {'sessionitems': session_items}
    # NOTE: I think it should be fine passing a list - the important thing is that it's an iterable


#this to template tags below are to get all the offers user is involved in
@register.inclusion_tag('market/offer_snip.html')
def get_your_offers(yourID):
    allOffers = Offer.objects.filter(fromID__exact=yourID).values('offerID').values()
    allOffersParsed = []
    for offer in allOffers:
        recieverID = offer['toID_id']
        reciever = UserProfile.objects.get(userID__exact=int(recieverID))
        offer['toID_id']=reciever.user.username
        allOffersParsed += [offer]
    return {'yourOffers':allOffersParsed}


@register.inclusion_tag('market/offer_snip.html')
def get_to_you_offers(yourID):  #this method should return all tradable and nontradable Items
    allOffers = Offer.objects.filter(toID__exact=yourID).values('offerID').values()
    #sende
    allOffersParsed = []
    for offer in allOffers:
        #llOffersParsed += [offer]
        senderID = offer['fromID_id']
        sender = UserProfile.objects.get(userID__exact=int(senderID))
        offer['fromID_id']=sender.user.username
        allOffersParsed += [offer]
    return {'toYouOffers':allOffersParsed}
