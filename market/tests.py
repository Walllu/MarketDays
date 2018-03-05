# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

class ModelTests(TestCase):
    
    # A test to see if the database population goes well
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
    
    # helper functions that will be used to check existence of objects 

    # funtion to query user db by username
    def get_user(self, **kwargs):
        from market.models import UserProfile
        try:
            keys = kwargs.keys()
            # accept only 1 keyword argument
            if ((len(keys)>1) or (len(keys)==0)):
                return None
            key = keys[0]
            if (key=="userID"): # if searching by userID
                user = UserProfile.objects.get(userID=kwargs[key])
            elif (key=="userName"):
                user = UserProfile.objects.get(userName=kwargs[key])
            elif (key=="firstName"):
                user = UserProfile.objects.get(firstName=kwargs[key])
            elif (key=="lastName"):
                user = UserProfile.objects.get(lastName=kwargs[key])
            else:
                print "Unrecognized kwarg in get_user"
                return None
        except UserProfile.DoesNotExist:
            user = None
        return user
    
    def get_item(self, **kwargs):
        from market.models import Item
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

    # suite of Model tests
    # tests for UserProfile
    # test existence
    def test_is_a_user(self):
        # just chose a random userID that you know should be in the db
        user1 = self.get_user(userID = 978)
        self.assertIsNotNone(user1)
        # choose a username you know should be in the db
        user2 = self.get_user(userName = 'rcraik4')
        self.assertIsNotNone(user2)
        # choose a first name you know should be in the db
        user3 = self.get_user(firstName = 'Roger')
        self.assertIsNotNone(user3)
        # choose a lasat name you know should be in the db
        user4 = self.get_user(lastName = 'Tomlett')
        self.assertIsNotNone(user4)
    # tests for Item
    # test existence
    # 
    def test_is_an_item(self):
        item1 = self.get_item(itemID = 1)
        self.assertIsNotNone(item1)
        item2 = self.get_item(itemName = "chin")
        self.assertIsNotNone(item2)











class FormTests(TestCase):
    def setUp(self):
        try:
            from forms import LoginForm # we need to have a login form
            from forms import SignUpForm # we need to have a signup form
            from forms import AccountEditForm # we need to be able to edit account
        except ImportError:
            print "the forms modele does not exist"
        except NameError:
            print "The class []Form does not exist, or is incorrect"
        except:
            print "Something else went wrong in FormTests"

#    def test_does_login_form_exist(self):
        
