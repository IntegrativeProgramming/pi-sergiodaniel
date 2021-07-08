from django.test import TestCase
from django.test import Client
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth import *

from playlists.views import *

import requests

 
class LoginTestCase(TestCase):
        
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()
 
    def tearDown(self):
        self.user.delete()
 
    def test_login_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)
 
    def test_login_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)
 
    def test_login_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
 


class SpotifyAuthenticationTestCase(TestCase):
 
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()
 
    def tearDown(self):
        self.user.delete()
 
    def test_login_spotify(self):

        response = login_spotify("GET /playlists/login_spotify/ HTTP/1.1")
        self.assertEquals(response.status_code, 302)

        response2 = cerrarsesion(response)
        self.assertEquals(response2.status_code, 302)


    #def test_home_spotify(self):
     #   response = callback("GET /playlists/callback/ HTTP/1.1")
      #  self.assertEquals(response.status_code, 200)