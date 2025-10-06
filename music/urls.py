from django.urls import path

from . import views

app_name = "music"

urlpatterns = [    
    path('', views.homepage, name='home'),
    path('new-playlist', views.playlist_new, name='new-playlist'),
    path('playlist/', views.playlist, name='playlist'),
    path('about/', views.about, name='about'),
    path('playlist/<int:pk>/', views.playlist_view, name='playlist_view')
]