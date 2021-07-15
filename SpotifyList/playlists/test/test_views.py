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

    def test_grafico_canciones(self):
        c = Client()
        response_get = c.get('/playlists/grafico_canciones/')
        self.assertEquals(response_get.status_code, 200)

    def test_mostrar_playlists(self):
        c = Client()
        response = c.get('/playlists/mostrar_playlists/')
        self.assertEquals(response.status_code, 302)

    # def test_callback(self): FALLO HEADERS , FALTA UNO
    #     c = Client()
    #     response = c.get('/playlists/callback/',{'code':'safsadgfdsfagd', 'state':'sjfvhasdasfd'},{'header':'Basic kljxzbvds'})
    #     self.assertEquals(response.status_code, 302)

    # callback_genius

    # def test_home(self):
    #     c = Client()
    #     response = c.get('/playlists/home/', {'Authorization': preparedString})
    #     self.assertEquals(response.status_code, 200)   

    # def test_mostrar_tracks(self): 404
    #     c = Client()
    #     response = c.post('/playlists/mostrar_tracks/',{'track_name':'hola', 'nombre_playlist':'Rap Caviar' 
    #         ,'playlist_id':'47RwPX4akLGe6OqyGpcWMd'})
    #     self.assertEquals(response.status_code, 302)

    def test_add_playlist(self):
        client_id = '2e6a6b883a174b3693a4c0a335558f30'
        client_secret = 'a2fbd32563c04123a3515c45951206ca'
        auxString = '{}:{}'.format(client_id, client_secret)
        preparedString = base64.b64encode(auxString.encode()).decode()

        c = Client()

        response_get = c.get('/playlists/add_playlist/')
        self.assertEquals(response_get.status_code, 200)
        # response = c.post('/playlists/add_playlist/',
        #     {'playlist_name':'playlistTEST','playlist_description':'wakanda', 
        #     'playlist_type':'public'}, {'Authorization': preparedString},
        #     HTTP_ACCEPT='application/json')
        # self.assertEquals(response.status_code, 302)

    # def test_add_searched_playlist(self):
    #     c = Client()
    #     response_get = c.get('/playlists/add_searched_playlist/', 
    #         {'playlist_id':'2DiQ9JVYVSrJZVETtTLRpb', 'nombre_playlist':'ADISTA'})
    #     self.assertEquals(response_get.status_code, 200)


    # def test_playlist_detail(self):
    #     c = Client()
    #     response = c.get('/playlists/playlist_detail/2DiQ9JVYVSrJZVETtTLRpb/ADISTA/' )
    #     self.assertEquals(response.status_code, 302)


    # def test_info_artista(self):
    #     c = Client()
    #     response = c.get('/playlists/info_artista/', {'track_name': 'hola'})
    #     self.assertEquals(response.status_code, 200)