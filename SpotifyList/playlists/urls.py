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
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),
    url(r'^show_playlists/$', views.show_playlists, name='show_playlists'),
    url(r'^view_playlist_info/(?P<playlistId>\w+)/(?P<playlistName>.*)/$', views.view_playlist_info, name='view_playlist_info'),

]
