# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    userID = models.OneToOneField(User)
    userPhoneNumber = models.IntegerField(default=0)
    userPicture = models.ImageField(upload_to='profile_images', blank=True)
    userDescribtion = models.CharField(max_length=512, unique=True)
    userInterests = models.CharField(max_length=512, unique=True)
    userStartDate = models.DateField(_("Date"), default=datetime.date.today)
    #creditcard to model later

    def __str__(self):
        return self.user.username


class Item(models.Model):
    posterID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    currentOwnerId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=128)
    itemPicture = models.ImageField(upload_to='profile_images', blank=True)
    itemDescription = models.CharField(max_length=512, unique=True)
    itemDatePosted = models.DateField(_("Date"), default=datetime.date.today)
    #itemValue

#note for the future, we should sort out an way on deleting offers when somebody exit session
class Offer(models.Model):
    offerID = models.IntegerField(default=0, unique=True)
    fromID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    toID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    offerTimeStamp = models.DateField(_("Date"), default=datetime.date.today)


class Session(models.Model):
    sessionID = models.IntegerField(default=0, unique=True)
    sessionName = models.CharField(max_length=32)
    xCords = models.IntegerField(default=0)
    yCords = models.IntegerField(default=0)
    sessionStart = models.DateField(_("Date"), default=datetime.date.today)
    sessionEnd = models.DateField(_("Date"), default=datetime.date.today)


class OfferContent(models.Model):
    callerID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    caleeID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.PROTECT)
    offerID = models.ForeignKey(Offer, on_delete=models.CASCADE)

    
class SessionParticipants(models.Model):
    sessionId = models.ForeignKey(Session, on_delete=models.PROTECT)
    participantID = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    
         
    
