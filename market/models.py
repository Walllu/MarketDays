# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import datetime # this wasn't imported, DateField's broke

# Create your models here.

class UserProfile(models.Model):
    userID = models.OneToOneField(User)
    userPhoneNumber = models.IntegerField(default=0)
    userPicture = models.ImageField(upload_to='profile_images', blank=True)
    userDescription = models.CharField(max_length=512, unique=True)
    userInterests = models.CharField(max_length=512, unique=True)
    userStartDate = models.DateField(_("Date"), default=datetime.date.today)
    #creditcard to model later

    def __str__(self):
        return self.user.username


class Item(models.Model):
    posterID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    currentOwnerId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)         #Why is this CASCADE? Walter 26.2.2018
    itemName = models.CharField(max_length=128)
    itemPicture = models.ImageField(upload_to='profile_images', blank=True)
    itemDescription = models.CharField(max_length=512, unique=True)                   #Why is this unique? Surely we can have non-unique descriptions  Walter 26.2.2018
    itemDatePosted = models.DateField(_("Date"), default=datetime.date.today)
    #itemValue

#note for the future, we should sort out an way on deleting offers when somebody exit session
class Offer(models.Model):
    offerID = models.IntegerField(default=0, unique=True)
    fromID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    toID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)               #why is this CASCADE?   Walter 26.2.2018
    message = models.CharField(max_length=256)
    offerTimeStamp = models.DateField(_("Date"), default=datetime.date.today)  
     
    class Meta:
        verbose_name_plural = 'offers'

    #def __str__(self):
        #Walter 26.2.2018 Added a few of these __str__ classes - I aimed to make them meaningful
     #   return str(self.offerID)+"-from-"+str(self.fromID)+"-to-"+str(self.toID)+"-@"+str(self.offerTimeStamp)


class Session(models.Model):
    sessionID = models.IntegerField(default=0, unique=True)
    sessionName = models.CharField(max_length=32)
    xCords = models.IntegerField(default=0)
    yCords = models.IntegerField(default=0)
    sessionStart = models.DateField(_("Date"), default=datetime.date.today)
    sessionEnd = models.DateField(_("Date"), default=datetime.date.today)

    class Meta:
        verbose_name_plural = 'sessions'

    #def __str__(self):
    #    return str(self.sessionID)+"-title-"+str(self.sessionName)


class OfferContent(models.Model):
    callerID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    calleeID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)      #Why is this CASCADE? Walter 26.2.2018
    itemID = models.ForeignKey(Item, on_delete=models.PROTECT)
    offerID = models.ForeignKey(Offer, on_delete=models.CASCADE)             #Why is this CASCADE? Walter 26.2.2018

   # def __str__(self):
   #     return str(self.callerID)+"-"str(self.calleeID)+"-"+str(self.itemID)+"-"+str(self.offerID)

    
class SessionParticipants(models.Model):
    sessionId = models.ForeignKey(Session, on_delete=models.PROTECT)
    participantID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)

    #def __str__(self):
    #    return str(self.sessionID)+"-participant-"+str(self.participantID)
    
         
    
