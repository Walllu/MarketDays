# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from market.models import UserProfile, Item, Offer, Session, OfferContent, SessionParticipants
# Register your models here.


# Walter 26.2.2018
# Someone have a think about if we need a UserAdmin class


class UserProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('userName',)}

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('itemID',)}

class OfferAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('offerID',)}

class SessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('sessionName',)}

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferContent)
admin.site.register(SessionParticipants)
