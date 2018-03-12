# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from market.models import Session, Item, UserProfile, Offer, OfferContent, SessionParticipants
import datetime

class UserProfileTests(TestCase):
    # this sets up the test database ONCE
    @classmethod
    def setUpTestData(cls):
        print "UserProfile Model tests commencing..."
        try:
            from populate import populate
            print "populating test database.........."
            populate()
        except ImportError:
            print "The module populate.py does not exist"
        except NameError:
            print "The function populate() does not exist, or is incorrect"
        except:
            print "Something fucked up in the population script"

    def setUp(self):
        pass

    # test existence
    def test_is_a_user(self):
        user1 = UserProfile.objects.get(userID=978)
        user2 = UserProfile.objects.get(userName='rcraik4')
        user3 = UserProfile.objects.get(firstName='Roger')
        user4 = UserProfile.objects.get(lastName='Tomlett')
        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertIsNotNone(user3)
        self.assertIsNotNone(user4)

    # test startdate can't be in the future
    def test_user_joined_cant_be_in_the_future(self):
        futuretime = datetime.datetime.now()+datetime.timedelta(days=30)
        user = UserProfile(userID=1000, userName="aassss", firstName="Billy", lastName="Joel", email="billy@joel.org", userStartDate=futuretime)
        #self.assertRaises() # not quite sure what exception is raised here

    # test that slug creation works fine
    def test_slug_works(self):
        user = UserProfile(userID=1001, userName="FaLLaFeLs", firstName="Bob", lastName="Bobb", email="bob@bob.com")
        user.save()
        self.assertEqual(user.slug, 'fallafels') # these might not be unique, what!
    # test that





class OfferTests(TestCase):
    #come up with a shorter setUp
    @classmethod
    def setUpTestData(cls):
        print "Offer Model tests commencing..."
        try:
            from populate import populate
            print "populating test database.........."
            populate()
        except ImportError:
            print "The module populate.py does not exist"
        except NameError:
            print "The function populate() does not exist, or is incorrect"
        except:
            print "Something fucked up in the population script"

    def setUp(self):
        pass

    # test that offer creation works
    def test_offer_creation(self):
        user1 = UserProfile.objects.get(userID=1)
        user2 = UserProfile.objects.get(userID=2)
        offer = Offer()



    # test that an offer can't be made from someone else
    def test_offer_creation_from_user(self):
        pass
    # test that an offer must be sent to an existing user
    def test_offer_needs_to_go_to_existing_user(self):
        pass
    # test that an offer can't be made in the future
    def test_offer_cant_be_made_in_future(self):
        pass
    # test that an offer's sender info is preserved
    def test_offer_sender_info_is_preserved(self):
        pass
    # test that an offer's reciever info is preserved
    def test_offer_receiver_info_is_preserved(self):
        pass
    # test that an item can only be offered if it exists
    def test_item_contents_must_exist(self):
        pass
    # test that

class SessionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print "Session Model tests commencing..."
        try:
            from populate import populate
            print "populating test database.........."
            populate()
        except ImportError:
            print "The module populate.py does not exist"
        except NameError:
            print "The function populate() does not exist, or is incorrect"
        except:
            print "Something fucked up in the population script"

    # define a new session to test
    def setUp(self):
        testSession = Session(sessionID=22, sessionName="Session 22", sessionStart=datetime.datetime.now(), sessionEnd=datetime.datetime.now()+datetime.timedelta(days=1))
        testSession.save()

    # test that sessionID is unique
    def test_session_is_unique(self):
        pass
    # test that a session can't start and end at the same time
    def test_session_cant_be_zero_time(self):
        pass
    # test that a session can't end before it starts
    def test_session_cant_end_before_it_starts(self):
        pass
    # test that a session can't start in the past
    def test_session_cant_start_in_the_past(self):
        pastdate = datetime.datetime.now() - datetime.timedelta(days=-30)
        session = Session(sessionID=15, sessionName="New Sesh", sessionEnd=pastdate)
        #self.assertEqual
    # test that a session can't end in the past
    # test that a session can't have negative number of participants
    # test that the session participant number increases with participants
    # test that the session participant number decreases when participant leaves
    # test that participant is actually a participant in that session
    # test that a participant can't be part of more than one session
    # test that a participant can't join a session that doesn't exist



class ItemTests(TestCase):
    def setUp(self):
        try:
            from populate import populate
            print "populating test database.........."
            populate()
        except ImportError:
            print "The module populate.py does not exist"
        except NameError:
            print "The function populate() does not exist, or is incorrect"
        except:
            print "Something fucked up in the population script"

    def get_item(self, **kwargs):
        try:
            keys=kwargs.keys()
            if((len(keys)==0) or (len(keys)>1)):
                return None
            key = keys[0]
            if (key=="itemID"):
                item = Item.objects.get(itemID=kwargs[key])
            elif (key=="itemName"):
                item = Item.objects.get(itemName=kwargs[key])
            else:
                print "Unrecognized kwarg in get_item"
                return None
        except Item.DoesNotExist:
            item = None
        return item
    # test existence
    def test_is_an_item(self):
        item1 = self.get_item(itemID = 1)
        self.assertIsNotNone(item1)
        item2 = self.get_item(itemName = "chin")
        self.assertIsNotNone(item2)

    # test that ownerID has to be existing user
    def test_ownerID_must_exist(self):
        pass
    # test that claimantID has to be existing user
    def test_claimantID_must_exist(self):
        pass
    # test that itemDatePosed can't be in the future
    def test_item_cant_be_made_in_the_future(self):
        futuretime = datetime.datetime.now() + datetime.timedelta(days=30)
        #item = Item(itemID=1, possessorID=1, claimantID=1, itemName="test", itemDescription="",itemDatePosted=futuretime)
