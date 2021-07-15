from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, response
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
import matplotlib.pyplot as plt
import seaborn as sns


# Create your views here.

# http://127.0.0.1:8000/playlists/signup_view/

client_id = '2e6a6b883a174b3693a4c0a335558f30'
client_secret = 'a2fbd32563c04123a3515c45951206ca'

client_id_genius = '32rQ76BgBmmx4rvsiPpf8LstvrOQmyLJq6kCRMEM1PCqa2JRZX7z1n4WRRFuISkZ'
client_secret_genius = '56Y-GmGryi7cTNmDf3dZj-CzvFeCaIjoY_DFljpwnVENRjYPH8NMg0IhGWRjUFWIwhS4MZ1Wh5fqspnO4e-16Q'


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
            
            url = 'http://127.0.0.1:8000/playlists/info_artista/' + request.session['aux_trackName']

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
        isEmpty = False
        songs = []
        data = r.json()

        for items in data:
            if items == 'items':
                for ptrack in data[items]:
                    isEmpty = True
                    for artists in ptrack['track']['artists']:
                        artists_names = artists['name']
                    min, sec = divmod(ptrack['track']['duration_ms']/1000, 60)                   
                    songs.append({'nombre': ptrack['track']['name'], 'artista': artists_names,
                                                    'artist_id': artists['id'],
                                                    'album': ptrack['track']['album']['name'],
                                                    'duracion': f'{min:0>2.0f}:{sec:2.0f}',
                                                    'popularidad': ptrack['track']['popularity'],
                                                    'link': ptrack['track']['external_urls']['spotify'],
                                                    'track_uri': ptrack['track']['uri']})

        if isEmpty:
            frame=pd.DataFrame(songs,columns=['nombre', 'popularidad'])
            frame_sort= frame.sort_values('popularidad', ascending=False)
            frame5 = frame_sort[:5]

            sns.set(font_scale=4)

            f, ax = plt.subplots(figsize=(50, 30))
            f.subplots_adjust(left=0.35)

            sns.barplot(x="popularidad", y="nombre", data=frame5,
                            label="Popularidad", color="c")
            ax.set(xlim=(0, 100),
                    xlabel="Popularidad", ylabel='Nombre de la cancion')

            plt.savefig('playlists/static/grafica.png')

        context = {
            'playlist_id': playlist_id, 
            'nombre_playlist': nombre_playlist,
            'array_table_elements': songs,
            'empty_playlist': isEmpty
        }

        return render(request, 'playlists/playlist_detail.html', context)
    else:
        return HttpResponseForbidden


def grafico_canciones(request):

    return render(request, 'playlists/grafico_canciones.html')


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


def delete_track(request, playlist_id, track_uri, nombre_playlist):
    
    headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(request.session['access_token']),
            'Content-Type': 'application/json',
        }
    
    data = '{"tracks":[{"uri":"'+ track_uri +'","positions":[0]}]}'  

    r = requests.delete('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id), headers=headers, data=data)

    if r.status_code == 200:
        return redirect('playlist_detail', playlist_id, nombre_playlist)
    else:
        return HttpResponseServerError


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


def mostrar_tracks(request, nombre_playlist, playlist_id):

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
            info_tracks = pd.DataFrame(r.json()['tracks']['items'], columns=['name', 'artists', 'album', 'duration_ms','popularity', 'external_urls', 'uri'])          

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
                                                'link': items['external_urls']['spotify'],
                                                'uri': items['uri']})

            context = {
                'search_track_name': request.POST['track_name'],
                'owned_playlist_name': nombre_playlist,
                'playlist_id': playlist_id,
                'array_table_elements': tracks_info
            }

            return render(request, 'playlists/mostrar_tracks.html', context)
        else:
            return HttpResponseServerError
    else:
        return HttpResponseServerError


def add_track(request, track_id, nombre_track, nombre_playlist, playlist_id):

    request.session['track_name'] = nombre_track

    headers = {
        'Authorization': 'Bearer {}'.format(request.session['access_token'])
    }

    url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id) + "?uris=" + track_id

    r = requests.post(url, headers=headers)

    if r.status_code == 201:

        context = {'track_name': nombre_track,
                   'playlist_id': playlist_id,
                   'playlist_name': nombre_playlist}
        return render(request, 'playlists/add_track_search.html', context)
    else:
        return HttpResponseServerError


def add_searched_playlist(request, playlist_id, nombre_playlist):

    request.session['nombre_playlist'] = nombre_playlist

    headers = {
        'Authorization': 'Bearer {}'.format(request.session['access_token']),
        'Content-Type': 'application/json',
    }

    url = 'https://api.spotify.com/v1/playlists/{}/followers'.format(playlist_id)

    r=requests.put(url, headers=headers)

    if r.status_code == 200:

        context = {'playlist_name': nombre_playlist,
                   'playlist_id': playlist_id}
        return render(request, 'playlists/add_playlist_search.html', context)
    else:
        return HttpResponseServerError


def info_artista(request, track_name):

    try:
        request.session['genius_access_token']
        geniusLogin = True
        trackName = track_name
        del request.session['aux_trackName']
    except:
        request.session['aux_trackName'] = track_name
        return redirect('login_genius')

    if geniusLogin:

        array_table_elements = []

        query_string = {
            'q': trackName
        }

        headers = {
            'Authorization': 'Bearer {}'.format(request.session['genius_access_token'])
        }

        r = requests.get('https://api.genius.com/search?' + urllib.parse.urlencode(query_string), headers=headers)

        if r.status_code == 200:
            genius_artist_id = None
            for result in r.json()['response']['hits']:
                genius_artist_id = result['result']['primary_artist']['id']
                break

            headers = {
                'Authorization': 'Bearer {}'.format(request.session['genius_access_token'])
            }

            if genius_artist_id != None:
                r = requests.get('https://api.genius.com/artists/' + str(genius_artist_id),
                                    headers=headers)

                if r.status_code == 200:
                    data = r.json()['response']['artist']
                    array_table_elements.append({'name': data['name'], 'followers' : data['followers_count'],
                                    'image': data['image_url'], 'facebook_name': data['facebook_name'],
                                    'instagram_name': data['instagram_name'], 'twitter_name': data['twitter_name']})
        
        context = {
            'array_table_elements': array_table_elements,
            'geniusLogin': geniusLogin,
        }

        return render(request, 'playlists/instagram_artista.html', context)

    else:
        return HttpResponseServerError