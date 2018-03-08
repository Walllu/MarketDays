# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase


# Create your tests here.


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
