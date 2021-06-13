from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from playlists.forms import LoginForm, SignupForm, AddPlayListForm


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


def login_genius(request):

    state = gen_state(16)

    scope = 'me create_annotation'
    query_string = {
        'response_type': 'code',
        'client_id': client_id_genius,
        'scope': scope,
        'redirect_uri': redirect_uri_genius,
        'state': state
    }

    response = redirect('https://api.genius.com/oauth/authorize?' + urllib.parse.urlencode(query_string))
    response.set_cookie('stateKey', state)

    return response



def callback(request):

    code = request.GET['code']
    state = request.GET['state']
    storedState = None

    print(request.COOKIES)

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


def callback_genius(request):

    code = request.GET['code']
    state = request.GET['state']
    storedState = None

    if request.COOKIES:
        storedState = request.COOKIES['stateKey']

    if state is None or state != storedState:
        return HttpResponseServerError
    else:
        request.COOKIES.clear()

        url = 'https://api.genius.com/oauth/token'

        form = {
            'code': code,
            'client_id': client_id_genius,
            'client_secret': client_secret_genius,
            'redirect_uri': redirect_uri_genius,
            'response_type': "code",
            'grant_type': 'authorization_code',
        }

        r = requests.post(url, data=form)

        if r.status_code == 200:

            access_token = r.json()['access_token']

            request.session['genius_access_token'] = access_token

            url = 'http://127.0.0.1:8000/miSpotify/view_artist_info/' + request.session['aux_artistId'] + '/?trackName=' + request.session['aux_trackName']

            return redirect(url)

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

            context = {
                'array_table_elements': playlists
            }

            return render(request, 'playlists/home.html', context)
        else:
            return HttpResponseForbidden

def playlist_detail(request, playlist_id, nombre_playlist):

    headers = {
            'Authorization': 'Bearer {}'.format(request.session['access_token'])
        }

    r = requests.get('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id), headers=headers)

    if r.status_code == 200:

        songs = []
        data = r.json()

        for items in data:
            if items == 'items':
                for ptrack in data[items]:
                    for artists in ptrack['track']['artists']:
                        artists_names = artists['name']
                    min, sec = divmod(ptrack['track']['duration_ms']/1000, 60)                   
                    songs.append({'nombre': ptrack['track']['name'], 'artista': artists_names,
                                                    'album': ptrack['track']['album']['name'],
                                                    'duracion': f'{min:0>2.0f}:{sec:2.0f}',
                                                    'popularidad': ptrack['track']['popularity'],
                                                    'link': ptrack['track']['external_urls']['spotify']})


        context = {
            'playlist_id': playlist_id, 
            'nombre': nombre_playlist,
            'array_table_elements': songs
        }

        return render(request, 'playlists/playlist_detail.html', context)
    else:
        return HttpResponseForbidden



def add_playlist(request):

    if 'playlist_name' in request.POST:
        playlist_name = request.POST['playlist_name']
        playlist_description = request.POST['playlist_description']
        playlist_type = request.POST['playlist_type']

        if playlist_type == 1:
            public = True
        else:
            public = False

        form = {
            'name': playlist_name,
            'public': public,
            'description': playlist_description
        }

        headers = {
            'Authorization': 'Bearer {}'.format(request.session['access_token']),
            'Content-Type': 'application/json'
        }

        r = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(request.session['user_id']), headers=headers, json=form)

        if r.status_code == 201:
            return redirect('home')
        else:
            return HttpResponseServerError
    else:
        add_play_list = AddPlayListForm()

        context = {'add_playlist_form': add_play_list}
        return render(request, 'playlists/addPlaylist.html', context)


def delete_playlists(request, playlist_id):
    r = request.delete('https://api.spotify.com/v1/playlists/{playlist_id}/tracks'.format(request.session['user_id']), headers=headers, json=form)


def delete_tracks(request, playlist_id):
    r = request.delete('https://api.spotify.com/v1/playlists/{playlist_id}/tracks'.format(request.session['user_id']), headers=headers, json=form)



def buscar(request, playlist_id, nombre_playlist):

    request.session['playlist_id'] = playlist_id
    request.session['ownedPlaylistName'] = nombre_playlist
    search_track_form = BusquedaForm()

    context = {
        'search_track_form': search_track_form,
        'playList_id': playlist_id
    }
    return render(request, 'miSpotify/nombre.html', context)


def mostrar_playlists(request):

    if 'nombre_playlist' in request.POST and request.POST['nombre_playlist'] != "":


        query_string = {
            'q': request.POST['nombre_playlist'],
            'type': 'playlist',
            'limit': 10
        }

        headers = {
            'Authorization': 'Bearer {}'.format(request.session['access_token'])
        }

        r = requests.get('https://api.spotify.com/v1/search?' + urllib.parse.urlencode(query_string), headers=headers)

        if r.status_code == 200:
            info_playlists = pd.DataFrame(r.json()['playlists']['items'], columns=['id','name', 'owner', 'description', 'external_urls', 'tracks'])
            playlists = []

            for i, items in info_playlists.iterrows():
                        playlists.append({'playlist_id': items['id'], 'nombre': items['name'], 'dueño': items['owner']['display_name'],
                                                     'descripcion': items['description'], 'link': items['external_urls']['spotify'], 'canciones': items['tracks']['total']})

            context = {
                'nombre_playlist':request.POST['nombre_playlist'],
                'array_table_elements': playlists
            }

            return render(request, 'playlists/mostrar_playlists.html', context)
        else:
            return HttpResponseServerError
    else:
        return redirect("home")


def mostrar_tracks(request):

    if 'track_name' in request.POST:

        query_string = {
            'q': request.POST['track_name'],
            'type': 'track',
            'limit': 10
        }

        headers = {
            'Authorization': 'Bearer {}'.format(request.session['access_token'])
        }

        r = requests.get('https://api.spotify.com/v1/search?' + urllib.parse.urlencode(query_string), headers=headers)

        if r.status_code == 200:
            info_tracks = pd.DataFrame(r.json()['tracks']['items'], columns=['name', 'artists', 'album', 'duration_ms','popularity', 'external_urls'])          

            info_tracks['duration_ms'] = info_tracks['duration_ms']/1000/60
            info_tracks['duration_ms'] = info_tracks['duration_ms'].round(2)
            info_tracks['duration_ms'] = info_tracks['duration_ms']

            tracks_info = []

            for i, items in info_tracks.iterrows():                 
                tracks_info.append({'nombre': items['name'],
                                                'artista': items['artists'][0]['name'],
                                                'album': items['album']['name'],
                                                'duracion': items['duration_ms'],
                                                'popularidad': items['popularity'],
                                                'link': items['external_urls']['spotify']})

            context = {
                'search_track_name': request.POST['track_name'],
                #'owned_playlist_name': request.session['ownedPlaylistName'],
                'array_table_elements': tracks_info
            }

            return render(request, 'playlists/mostrar_tracks.html', context)
        else:
            return HttpResponseServerError
    else:
        return HttpResponseServerError