# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders



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
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/profile.html')

class SessionListPageTests(TestCase):
    def test_session_list_uses_template(self):
        response = self.client.get(reverse('sessionlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/sessionlist.html')
