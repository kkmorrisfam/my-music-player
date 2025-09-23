from django.shortcuts import render
from .models import Album, Track, Artist

# this is referred to in urls.py
# path('', views.homepage),
def homepage(request):
    # albums = Album.objects.all()    
    # data = {'albums': albums}
    tracks = Track.objects.all()
    data = {'tracks': tracks}
    return render(request, 'index.html', data)

def playlist(request):
    return render(request, 'playlist.html')

def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],