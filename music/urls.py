from django.urls import path

from . import views

app_name = "music"

urlpatterns = [    
    path('', views.homepage, name='home'),
    path('new_playlist/', views.playlist_new, name='new_playlist'),
    path('playlist/', views.playlist, name='playlist'),
    path('about/', views.about, name='about'),
    path('playlist/<int:pk>/', views.playlist_view, name='playlist_view'),
    path('playlist/<int:pk>/composer/', views.playlist_composer, name='playlist_composer'),
    path('playlist/<int:pk>/items/', views.playlist_items, name='playlist_items'),
    path('playlist/<int:pk>/add/', views.playlist_add_track, name='playlist_add_track'),
    path('playlist/<int:pk>/search/', views.track_search, name='track_search'),
    path("playlist/<int:pk>/remove/", views.playlist_remove_track, name="playlist_remove_track"),
    path("playlist/<int:pk>/remove_playlist/", views.remove_playlist, name="remove_playlist"),


]