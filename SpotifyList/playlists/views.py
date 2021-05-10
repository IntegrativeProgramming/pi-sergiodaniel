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

