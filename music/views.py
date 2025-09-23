from django.shortcuts import render
from .models import Album, Track, Artist

# this is referred to in urls.py
# path('', views.homepage),
def homepage(request):
    # albums = Album.objects.all()    
    # data = {'albums': albums}
    # using prefetch_related instead of all, takes it down from 47 queries to just 2 with only "albums", adds one for each table fetching from
    # tracks = Track.objects.prefetch_related('albums', 'artists')
    tracks = Track.objects.filter(title__istartswith="t").prefetch_related('albums', 'artists')
    data = {'tracks': tracks}
    return render(request, 'index.html', data)

def playlist(request):
    return render(request, 'playlist.html')

def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],