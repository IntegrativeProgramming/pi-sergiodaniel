from django.test import TestCase
from django.test import Client


from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth import *
#from django.utils.importlib import import_module
from django.conf import settings

from playlists.views import *

import requests
 
# class LoginTestCase(TestCase):
        
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test', password='12test12')
#         self.user.save()
 
#     def tearDown(self):
#         self.user.delete()
 
#     def test_login_correct(self):
#         user = authenticate(username='test', password='12test12')
#         self.assertTrue((user is not None) and user.is_authenticated)
 
#     def test_login_wrong_username(self):
#         user = authenticate(username='wrong', password='12test12')
#         self.assertFalse(user is not None and user.is_authenticated)
 
#     def test_login_wrong_pssword(self):
#         user = authenticate(username='test', password='wrong')
#         self.assertFalse(user is not None and user.is_authenticated)
 

class TestsUsingClient(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    def test_login(self):
        c = Client()
        response = c.login(username='test', password='12test12')
        self.assertEquals(response, True)

    def test_cerrarsesion(self):
        c = Client()
        response = c.get('/playlists/cerrarsesion/')
        self.assertEquals(response.status_code, 302)

    def test_login_spotify_genius(self):
        c = Client()
        response = c.get('/playlists/login_spotify/')
        self.assertEquals(response.status_code, 302)

        response2 = c.get('/playlists/login_genius/')
        self.assertEquals(response2.status_code, 302)

    def test_callback(self):
        c = Client()
        response = c.get('/playlists/callback/',{'code':'safsadgfdsfagd', 'state':'sjfvhasdasfd'},{'Authorization':'holiii'})
        self.assertEquals(response.status_code, 302)

    # def test_info_artista(self):
    #     c = Client()
    #     response = c.get('/playlists/info_artista/', {'track_name': 'hola'})
    #     self.assertEquals(response.status_code, 200)