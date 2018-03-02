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
            elif (keys[0]=="userID"): # if searching by userID
                user = UserProfile.objects.get(userID=kwargs[keys[0]])
            elif (keys[0]=="userName"):
                user = UserProfile.objects.get(userName=kwargs[keys[0]])
            elif (keys[0]=="firstName"):
                user = UserProfile.objects.get(firstName=kwargs[keys[0]])
            else:
                print "Unrecognized kwarg"
                return None
        except UserProfile.DoesNotExist:
            user = None
        return user


    

    # suite of Model tests

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


