from django.test import TestCase
from django.test import Client
from importlib import import_module


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

    def test_grafico_canciones(self):
        c = Client()
        response_get = c.get('/playlists/grafico_canciones/')
        self.assertEquals(response_get.status_code, 200)

    def test_mostrar_playlists(self):
        c = Client()
        response = c.get('/playlists/mostrar_playlists/')
        self.assertEquals(response.status_code, 302)

    def test_add_playlist(self):
        c = Client()
        response_get = c.get('/playlists/add_playlist/')
        self.assertEquals(response_get.status_code, 200)

        response = c.post('/playlists/add_playlist/',
        {'name': 'playlistTEST', 'public': False, 'description': 'wakanda'}
        , HTTP_ACCEPT='application/json')
        self.assertEquals(response.status_code, 200)


# PROBLEMA HTML BOTON???

    # def test_mostrar_tracks(self):
    #     c = Client()
    #     response = c.post('/playlists/mostrar_tracks/ADISTA/2DiQ9JVYVSrJZVETtTLRpb/')
    #     self.assertEquals(response.status_code, 302)


    # def test_info_artista(self):
    #     c = Client()
    #     response = c.get('/playlists/info_artista/', {'track_name': 'hola'})
    #     self.assertEquals(response.status_code, 200)



####### 401

    # def test_add_searched_playlist(self):
    #     c = Client()
    #     response_get = c.post('/playlists/add_searched_playlist/5Xkw0sFd5Y89K7kfrusZsf/Hola%20Beats%20Lofi/'
    #     , HTTP_ACCEPT='application/json')
    #     self.assertEquals(response_get.status_code, 200)


    # def test_playlist_detail(self): 
    #     c = Client()
    #     response = c.get('/playlists/playlist_detail/2DiQ9JVYVSrJZVETtTLRpb/ADISTA/')
    #     self.assertEquals(response.status_code, 302)


####### 400

    # def test_callback(self):
    #     c = Client()
    #     response = c.get('/playlists/callback/',{'code': 'safsadgfdsfagd', 
    #         'redirect_uri': 'http://127.0.0.1:8000/playlists/callback',
    #         'grant_type': 'authorization_code', 'state':'dhjdsavfhj'}
    #         , HTTP_ACCEPT='application/json')
    #     self.assertEquals(response.status_code, 302)