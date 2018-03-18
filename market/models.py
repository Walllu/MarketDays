# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext as _ #I'm not sure about this fix - it seems to have fixed the DateFields, but I'm not sure why. StackOverFlow told me:)
import datetime # this wasn't imported, DateField's broke
from django.utils import timezone

# Create your models here.

def user_profile_path(self, userID):
    print "userID: " + str(userID)
    return "profile_pictures/" + str(userID)

def item_picture_path(self, itemID):
    print "itemID: " + str(itemID)
    return "item_pictures/" + str(itemID)

class UserProfile(models.Model):

    # Changing email and username to foreign keys from the User model - Ole
    userID = models.IntegerField(primary_key=True, unique=True, default=0)
    user = models.OneToOneField(User) # Ole, 1st Mar
    # removing the password field as it is now handled by User model
    # password = models.CharField(max_length=100, default="")
    firstName = models.CharField(max_length=20) # Ole, 1st Mar
    lastName = models.CharField(max_length=20, blank=True, default="Anon")# added blank # Ole, 1st Mar
    picture = models.ImageField(upload_to=user_profile_path, default="/profile_pictures/cat.jpg")
    # email = models.ForeignKey(User, related_name="user_email") #Ole, 2nd Mar
    userPhoneNumber = models.CharField(max_length=15,default="")
    userDescription = models.CharField(max_length=512, default="", blank=True)
    userInterests = models.CharField(max_length=512, default="",  blank=True)
    userStartDate = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=40) #changed for tests
    #creditcard to model later



    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.userID)


class Item(models.Model):
    itemID = models.IntegerField(primary_key=True,default=0, unique=True)
    possessorID = models.ForeignKey(UserProfile, related_name='owns_physically', on_delete=models.CASCADE) # Cascade intent: If the user is deleted, delete the item
    claimantID = models.ForeignKey(UserProfile, related_name='owns_entitlement', on_delete=models.DO_NOTHING) # I think it makes sense that the item isn't deleted if the claimant account is deleted - Ole        #Why is this CASCADE? Walter 26.2.2018
    itemName = models.CharField(max_length=128)
    itemDescription = models.CharField(max_length=512, blank=True)                   #Why is this unique? Surely we can have non-unique descriptions  Walter 26.2.2018
    itemDatePosted = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=item_picture_path, default="/media/cat.jpg")
    slug = models.SlugField(unique=True)
    #itemValue

    def create_offer(self):
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.itemID)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.itemID)

#note for the future, we should sort out an way on deleting offers when somebody exit session
class Offer(models.Model):
    offerID = models.IntegerField(default=0, unique=True)
    fromID = models.ForeignKey(UserProfile, related_name='offer_maker', on_delete=models.CASCADE) # Intent: If a user account is deleted, their offers should also disappear
    toID = models.ForeignKey(UserProfile, related_name='offer_reciever', on_delete=models.CASCADE) # And the same for both sides of the offer               #why is this CASCADE?   Walter 26.2.2018
    message = models.CharField(max_length=256, blank=True)
    offerTimeStamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'offers'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.offerID)
        super(Offer, self).save(*args, **kwargs)
    #def __str__(self):
        #Walter 26.2.2018 Added a few of these __str__ classes - I aimed to make them meaningful
     #   return str(self.offerID)+"-from-"+str(self.fromID)+"-to-"+str(self.toID)+"-@"+str(self.offerTimeStamp)


class Session(models.Model):
    sessionID = models.IntegerField(default=0, unique=True)
    sessionName = models.CharField(max_length=32, unique=True)
    xCords = models.IntegerField(default=0)
    yCords = models.IntegerField(default=0)
    sessionStart = models.DateTimeField(default=timezone.now)
    sessionEnd = models.DateTimeField()
    participants = models.IntegerField(default=0) # Ole, 1st Mar
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'sessions'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sessionName)
        super(Session, self).save(*args, **kwargs)
    #def __str__(self):
    #    return str(self.sessionID)+"-title-"+str(self.sessionName)


class OfferContent(models.Model):
    callerID = models.ForeignKey(UserProfile, related_name='from_side_inventory', on_delete=models.PROTECT)
    calleeID = models.ForeignKey(UserProfile, related_name='to_side_inventory', on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
    offerID = models.ForeignKey(Offer, on_delete=models.CASCADE)
    offered = models.BooleanField()

   # def __str__(self):
   #     return str(self.callerID)+"-"str(self.calleeID)+"-"+str(self.itemID)+"-"+str(self.offerID)


class SessionParticipants(models.Model):
    sessionID = models.ForeignKey(Session, on_delete=models.PROTECT)
    participantID = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)

    #def __str__(self):
    #    return str(self.sessionID)+"-participant-"+str(self.participantID)
