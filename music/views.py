from django.shortcuts import render
from .models import Album, Track, Artist, Playlist, PlaylistTrack
from django.db.models.functions import Random
from django.db.models import Prefetch

# this is referred to in urls.py
# path('', views.homepage),
def homepage(request):
    # albums = Album.objects.all()    
    # data = {'albums': albums}
    # using prefetch_related instead of all, takes it down from 47 queries to just 2 with only "albums", adds one for each table fetching from
    # tracks = Track.objects.filter(title__istartswith="t").prefetch_related('albums', 'artists')
    
    tracks = (
        Track.objects 
        .order_by(Random())   
        .prefetch_related('albums', 'artists')
    )
    
    data = {'tracks': tracks}
    return render(request, 'index.html', data)


def playlist(request):
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user)
    
    return render(request, 'playlist.html', {"playlists": playlists})

# def playlist(request):
#     prefetch = Prefetch('playlisttrack_set', queryset=PlaylistTrack.objects
#                         .select_related('track')
#                         .ordered_by('position', 'id'),
#                         to_attr='items'
#                         )
#     if request.user.is_authenticated:
#         playlists = (Playlist.objects
#                      .filter(owner=request.user)
#                      .prefetch_related(prefetch)
#                      .order_by('name'))
        
    
#     return render(request, 'playlist.html', {"playlists": playlists})



def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],