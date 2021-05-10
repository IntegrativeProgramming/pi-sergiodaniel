from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from miSpotify.forms import LoginForm, SignupForm, AddPlayListForm, SearchTrackForm


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

client_id = '2e6a6b883a174b3693a4c0a335558f30'
client_secret = 'a2fbd32563c04123a3515c45951206ca'


redirect_uri = 'http://127.0.0.1:8000/playlists/callback'
redirect_uri_genius = 'http://127.0.0.1:8000/playlists/callback_genius'
redirect_uri_instagram = 'http://127.0.0.1:8000/playlists/callback_instagram'
redirect_uri_whatsapp = 'http://127.0.0.1:8000/playlists/callback_whatsapp'