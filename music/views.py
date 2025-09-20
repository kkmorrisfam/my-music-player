from django.shortcuts import render

# this is referred to in urls.py
# path('', views.homepage),
def homepage(request):
    return render(request, 'index.html')

def playlist(request):
    return render(request, 'playlist.html')

def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],