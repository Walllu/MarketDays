# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import datetime


class SessionListViewTest(TestCase):

    def setUp(self):


    def test_call_view_denies_anonymous(self):
        response = self.client.get('/market/sessionlist/', follow=True)
        self.assertRedirects(response, '/')
        response = self.client.post('/market/sessionlist/', follow=True)
        self.assertRedirects(response, '/')

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/market/sessionlist/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sessionlist.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/market/sessionlist', {})          # blank data dictionary
        self.assertFormError(response, 'form', 'some_field', 'This field is required.')
        # etc. ...

        """
    def test_call_view_fails_invalid(self):
        # as above, but with invalid rather than blank data in dictionary
        self.client.login(username='user', password='test')
        response = self.client.post('/market/sessionlist', {})          #invalid data dictionary
        self.assertFormError(response, 'form', 'some_field', 'This field is required.')


    def test_call_view_fails_invalid(self):
        # same again, but with valid data, then
        self.assertRedirects(response, '/contact/1/calls/')
        """
