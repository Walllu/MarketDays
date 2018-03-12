# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from market.models import *



class IndexPageTests(TestCase):
    def test_index_uses_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/index.html')

class AboutPageTests(TestCase):
    def test_about_uses_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/about.html')

class ProfilePageTests(TestCase):
    def test_profile_uses_template(self):
        response = self.client.get(reverse('userProfile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/userProfile.html')

class SessionListPageTests(TestCase):

    def setUp(self):
        user = User(username = "cofeenurd", password="1234", email="ayy@gmail.com", first_name="firstname", last_name="lastname")
        user.save()
        userprof = UserProfile(userID=1012, userName=user, firstName="firstname", lastName="lastname", email=user)
        userprof.save()

    def test_session_list_uses_template(self):
        self.client.login(username="cofeenurd", password="1234")
        response = self.client.get(reverse('sessionlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/sessionlist.html')
