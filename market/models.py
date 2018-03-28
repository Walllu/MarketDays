# -*- coding: utf-8 -*-


from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import datetime
from django.utils import timezone


def user_profile_path(self, userID):
    return "profile_pictures/" + str(userID)

def item_picture_path(self, itemID):
    return "item_pictures/" + str(itemID)

class UserProfile(models.Model):
    userID = models.IntegerField(primary_key=True, unique=True, default=0)
    user = models.OneToOneField(User)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20, blank=True, default="Anon")
    picture = models.ImageField(upload_to=user_profile_path, default="/media/profile_pictures/cat.jpg")
    userPhoneNumber = models.CharField(max_length=15,default="")
    userDescription = models.CharField(max_length=512, default="", blank=True)
    userInterests = models.CharField(max_length=512, default="",  blank=True)
    userStartDate = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.userID)


class Item(models.Model):
    itemID = models.IntegerField(primary_key=True,default=0, unique=True)
    possessorID = models.ForeignKey(UserProfile, related_name='owns_physically', on_delete=models.DO_NOTHING)
    claimantID = models.ForeignKey(UserProfile, related_name='owns_entitlement', on_delete=models.CASCADE)
    itemName = models.CharField(max_length=128)
    itemDescription = models.CharField(max_length=512, blank=True)
    itemDatePosted = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=item_picture_path, default="/media/cat.jpg")
    slug = models.SlugField(unique=True)

    def create_offer(self):
        pass

    def first(self):
        try:
            for test in self:
                 return test
        except:
            return self

    def save(self, *args, **kwargs):
        self.slug = slugify(self.itemID)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.itemID)
        

class Offer(models.Model):
    offerID = models.IntegerField(default=0, unique=True)
    fromID = models.ForeignKey(UserProfile, related_name='offer_maker', on_delete=models.CASCADE) # Intent: If a user account is deleted, their offers should also disappear
    toID = models.ForeignKey(UserProfile, related_name='offer_reciever', on_delete=models.CASCADE) # And the same for both sides of the offer
    message = models.CharField(max_length=256, blank=True)
    offerTimeStamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'offers'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.offerID)
        super(Offer, self).save(*args, **kwargs)
        

class Session(models.Model):
    sessionID = models.IntegerField(default=0, unique=True)
    sessionName = models.CharField(max_length=32, unique=True)
    xCords = models.IntegerField(default=0)
    yCords = models.IntegerField(default=0)
    sessionStart = models.DateTimeField(default=timezone.now)
    sessionEnd = models.DateTimeField()
    participants = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'sessions'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sessionName)
        super(Session, self).save(*args, **kwargs)


class OfferContent(models.Model):
    callerID = models.ForeignKey(UserProfile, related_name='from_side_inventory', on_delete=models.CASCADE)
    calleeID = models.ForeignKey(UserProfile, related_name='to_side_inventory', on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
    offerID = models.ForeignKey(Offer, on_delete=models.CASCADE)
    offered = models.BooleanField(default=True)


class SessionParticipants(models.Model):
    sessionID = models.ForeignKey(Session, on_delete=models.PROTECT)
    participantID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
