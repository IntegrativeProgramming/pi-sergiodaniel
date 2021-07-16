from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^iniciarsesion/$', views.iniciarsesion, name='iniciarsesion'),
    url(r'^cerrarsesion/$', views.cerrarsesion, name='cerrarsesion'),
    url(r'^login_spotify/$', views.login_spotify, name='login_spotify'),
    url(r'^login_genius/$', views.login_genius, name='login_genius'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^callback_genius/$', views.callback_genius, name='callback_genius'),
    url(r'^home/$', views.home, name='home'),
    url(r'^mostrar_tracks/(?P<nombre_playlist>.*)/(?P<playlist_id>.*)/$', views.mostrar_tracks, name='mostrar_tracks'),
    url(r'^mostrar_playlists/$', views.mostrar_playlists, name='mostrar_playlists'),
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),
    url(r'^add_track/(?P<track_id>[:\w]+)/(?P<nombre_track>.*)/(?P<nombre_playlist>.*)/(?P<playlist_id>.*)/$',  views.add_track, name='add_track'),
    url(r'^remove_track/(?P<playlist_id>[:\w]+)/(?P<track_uri>.*)/(?P<nombre_playlist>.*)/$', views.delete_track, name='delete_track'),
    url(r'^add_searched_playlist/(?P<playlist_id>[:\w]+)/(?P<nombre_playlist>.*)/$', views.add_searched_playlist, name='add_searched_playlist'),
    url(r'^grafico_canciones/$', views.grafico_canciones, name='grafico_canciones'),
    url(r'^info_artista/(?P<track_name>.*)/$', views.info_artista, name='info_artista'),
    url(r'^empty_playlist/(?P<playlist_id>[:\w]+)/$', views.empty_playlist, name='empty_playlist'),
    url(r'^playlist_detail/(?P<playlist_id>\w+)/(?P<nombre_playlist>.*)/$', views.playlist_detail, name='playlist_detail'),
]
