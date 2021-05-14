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

redirect_uri = 'http://127.0.0.1:8000/playlists/callback'
redirect_uri_genius = 'http://127.0.0.1:8000/playlists/callback_genius'
redirect_uri_instagram = 'http://127.0.0.1:8000/playlists/callback_instagram'
redirect_uri_whatsapp = 'http://127.0.0.1:8000/playlists/callback_whatsapp'


def signup_view(request):
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


def logout_view(request):
    logout(request)
    return redirect('index')

def _randomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def index(request):

    try:
        request.session.__contains__('error')
        del request.session['error']
        error = True
    except:
        error = False

    login_error1 = None
    login_error2 = None
    error_type = None

    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            login_error1 = "Ha ocurrido un error en el login."
            login_error2 = "Por favor, vuelva a intentarlo!"
            error_type = "login_error"
    elif error:
        login_error1 = "Ha ocurrido un error en el registro."
        login_error2 = "Por favor, vuelva a intentarlo!"
        error_type = "register_error"
    else:
        login_error1 = ""
        login_error2 = ""
        error_type = ""

    login_form = LoginForm()
    signup_form = SignupForm()
    if request.user.is_authenticated:
        return redirect('login_spotify')
    else:
        context = {'login_form': login_form, 'signup_form': signup_form, 'loginError1': login_error1,
                   'loginError2': login_error2, 'errorType': error_type}
        return render(request, 'playlists/login_content.html', context)



def login_spotify(request):

    state = _randomString(16)

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
        
        #try:
        #    del request.session["ownedPlaylistName"]
        #    del request.session['track_name']
        #    del request.session['playlistName']
        #except:
        #    pass

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
                        playlists.append({'name': playlist['name'], 'total': playlist['tracks']['total'],
                                                    'public': playlist['public'], 'playlist_id': playlist['id']})
                    break

            context = {
                'array_table_elements': playlists
            }

            return render(request, 'playlists/home.html', context)
        else:
            return HttpResponseForbidden