from django import template
from market.models import UserProfile, Session, Offer, Item

#Walter 26.2.2018
# This is just something here in case we want to use templatetags later on

register = template.Library()

# this is for the sessions list template
@register.inclusion_tag('market/sesh.html')
def get_session_list():
    return {'sessions': Session.objects.all()}

#I'm not entirely certain yet, but this might be a good place to put
#the query of getting all your items
# both for your account view
# but also for the haggle view

#@register_inclusion_tag('market/your_items.html')
#def get_your_items(yourID):
    #return {'youritems': Item.objects.filter(--)



#  Some suggested templatetags  --Walter 4.3.2018
#def get_their_items(theirID)
#def get_all_items():
#    return {'sessionitems': Item.objects.all()}
#def 



