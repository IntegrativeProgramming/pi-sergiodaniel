"""SpotifyList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^iniciarsesion/$', views.iniciarsesion, name='iniciarsesion'),
    url(r'^cerrarsesion/$', views.cerrarsesion, name='cerrarsesion'),
    url(r'^login_spotify/$', views.login_spotify, name='login_spotify'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^home/$', views.home, name='home'),
    url(r'^mostrar_tracks/(?P<nombre_playlist>.*)/(?P<playlist_id>.*)/$', views.mostrar_tracks, name='mostrar_tracks'),
    url(r'^mostrar_playlists/$', views.mostrar_playlists, name='mostrar_playlists'),
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),
    url(r'^add_track/(?P<track_id>[:\w]+)/(?P<nombre_track>.*)/(?P<nombre_playlist>.*)/(?P<playlist_id>.*)/$',  views.add_track, name='add_track'),
    url(r'^remove_track/(?P<playlist_id>[:\w]+)/(?P<track_uri>.*)/(?P<nombre_playlist>.*)/$', views.delete_track, name='delete_track'),
    url(r'^add_searched_playlist/(?P<playlist_id>[:\w]+)/(?P<nombre_playlist>.*)/$', views.add_searched_playlist, name='add_searched_playlist'),
    url(r'^playlist_detail(?P<playlist_id>\w+)/(?P<nombre_playlist>.*)/$', views.playlist_detail, name='playlist_detail'),
]
