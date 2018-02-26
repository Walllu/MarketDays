# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rango.models import UserProfile, Item, Offer, Session, OfferContent, SessionParticipants 
# Register your models here.


# Walter 26.2.2018
# Someone have a think about if we need a UserAdmin class
#class UserAdmin(admin.ModelAdmin):
#    pass 

class ItemAdmin(admin.ModelAdmin):
    list_display = ['posterID', 'currentOwnerID', 'itemName', 'itemDatePosted']

class OfferAdmin(admin.ModelAdmin):
    list_display = ['offerID', 'fromID', 'toID', 'message', 'offerTimeStamp']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['sessionID','sessionName', 'sessionStart', 'sessionEnd']

admin.site.register(Item, ItemAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserProfile)
admin.site.register(OfferContent)
admin.site.register(SessionParticipants)
