from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from playlists.forms import LoginForm, SignupForm


import requests
import random
import string
import urllib.parse
import base64
import oauth2 as oauth
import pandas as pd


# Create your views here.

# http://127.0.0.1:8000/playlists/signup_view/

client_id = '2e6a6b883a174b3693a4c0a335558f30'
client_secret = 'a2fbd32563c04123a3515c45951206ca'

client_id_genius = '8lIzMidCaMlcIVOeeW4WYeXYzFqv5qx3RJXra0k9qxyKO8hQai20eDqkWi_VR6s4'
client_secret_genius = '56Y-GmGryi7cTNmDf3dZj-CzvFeCaIjoY_DFljpwnVENRjYPH8NMg0IhGWRjUFWIwhS4MZ1Wh5fqspnO4e-16Q'

client_id_whatsapp = ''
client_secret_whatsapp = ''

client_id_instagram = ''
client_secret_instagram =''

redirect_uri = 'http://127.0.0.1:8000/playlists/callback'
redirect_uri_genius = 'http://127.0.0.1:8000/playlists/callback_genius'
redirect_uri_instagram = 'http://127.0.0.1:8000/playlists/callback_instagram'
redirect_uri_whatsapp = 'http://127.0.0.1:8000/playlists/callback_whatsapp'


def iniciarsesion(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            request.session['error'] = 'true'
            return redirect('index')
    else:
        return HttpResponseServerError


def cerrarsesion(request):
    logout(request)
    return redirect('index')

def gen_state(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def index(request):

    try:
        request.session.__contains__('error')
        del request.session['error']
        error = True
    except:
        error = False

    
    error_type = None

    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            error_type = "login_error"
    elif error:
        error_type = "register_error"
    
    login_form = LoginForm()
    signup_form = SignupForm()
    if request.user.is_authenticated:
        return redirect('login_spotify')
    else:
        context = {'login_form': login_form, 'signup_form': signup_form, 'errorType': error_type}
        return render(request, 'playlists/login_content.html', context)



def login_spotify(request):

    state = gen_state(16)

    scope = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private'
    query_string = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }

    response = redirect('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_string))
    response.set_cookie('stateKey', state)

    return response


def callback(request):

    code = request.GET['code']
    state = request.GET['state']
    storedState = None

    if request.COOKIES:
        storedState = request.COOKIES['stateKey']

    if state is None or state != storedState:
        return HttpResponseServerError
    else:
        request.COOKIES.clear()
        auxString = '{}:{}'.format(client_id, client_secret)
        preparedString = base64.b64encode(auxString.encode()).decode()

        url = 'https://accounts.spotify.com/api/token'

        form = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        headers = {
            'Authorization': 'Basic {}'.format(preparedString)
        }

        r = requests.post(url, data=form, headers=headers)

        if r.status_code == 200:

            access_token = r.json()['access_token']
            refresh_token = r.json()['refresh_token']

            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }

            r2 = requests.get('https://api.spotify.com/v1/me', headers=headers)

            if r2.status_code == 200:

                request.session['user_id'] = r2.json()['id']
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                return redirect('home')
            else:
                return HttpResponseServerError
        else:
            return HttpResponseServerError


def home(request):
        
        headers = {
            'Authorization': 'Bearer {}'.format(request.session['access_token'])
        }

        r = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)

        if r.status_code == 200:
            playlists = []

            data = r.json()
            for items in data:
                if items == 'items':
                    for playlist in data[items]:
                        playlists.append({'playlist_id': playlist['id'], 'nombre': playlist['name'], 'dueño': playlist['owner']['display_name'],
                                                     'descripcion': playlist['description'], 'link': playlist['external_urls']['spotify'], 'canciones': playlist['tracks']['total']})
                    break

            context = {
                'array_table_elements': playlists
            }

            return render(request, 'playlists/home.html', context)
        else:
            return HttpResponseForbidden

def playlist_detail(request, playlistId, playlistName):

    headers = {
        'Authorization': 'Bearer {}'.format(request.session['access_token'])
    }

    r = requests.get('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlistId), headers=headers)


    if r.status_code == 200:
        playlists = []

        array_table_elements = []
        data = r.json()
        for items in data:
            if items == 'items':
                for track in data[items]:
                    empty_playlist = True
                    for artists in track['track']['album']['artists']:
                        artists_name = artists['name']
                        duration_initial = track['track']
                        array_table_elements.append({'name': track['track']['name'], 'artist': artists_name,
                                                     'popularity': track['track']['popularity'],
                                                     'artist_id': artists['id']})
                        break
                break

        context = {
            'nombre_playlist': playlistName,
            'playList_id': playlistId,
            'array_table_elements': array_table_elements 
        }

        return render(request, 'playlists/playlist_detail.html', context)
    else:
        return HttpResponseForbidden

def add_playlist(request):
    print("add playlist mock")

def show_playlists(request):
    print("show playlists mock")

def view_playlist_info(request):
    print("view playlist mock")