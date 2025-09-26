from django.shortcuts import render, get_object_or_404
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

#explanation for this query - below code block
def playlist(request):
    prefetch = Prefetch("playlisttrack_set", queryset=(
                        PlaylistTrack.objects
                        .select_related('track')
                        .prefetch_related('track__albums','track__artists')
                        .order_by('position')
                        ), to_attr='pt_items'
               )
    
    playlists = Playlist.objects.none() #if not logged in, stays as none


    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user).prefetch_related(prefetch) 
    
    return render(request, 'playlist.html', {"playlists": playlists})

def playlist_view(request, pk):
    prefetch = Prefetch(
                        'playlisttrack_set', 
                        queryset=(
                            PlaylistTrack.objects
                            .select_related('track')
                            .prefetch_related('track__albums', 'track__artists')
                            .order_by('position', 'id')                            
                            ), to_attr='items'
                        )
    
    if request.user.is_authenticated:
        playlist = get_object_or_404(
                        Playlist.objects                     
                        .prefetch_related(prefetch),
                        pk=pk,
                        owner=request.user
                    )
    
    return render(request, 'playlist_view.html', {"playlist": playlist})



def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],


"""  
    Explanation of query in query for all playlists

Query 1: filter by owner

    (queryset)playlists = Playlist.objects.filter(owner=request.user)
    
    SELECT "music_playlist"."id",
        "music_playlist"."owner_id",
        "music_playlist"."name",
        "music_playlist"."created_at"
    FROM "music_playlist"
    WHERE "music_playlist"."owner_id" = 1

Query 2: get all playlist objects + joined tracks
    queryset=(PlaylistTrack.objects
                        .select_related('track')                        
                        .order_by('position')
                        )

    SELECT *
    FROM "music_playlisttrack"
    INNER JOIN "music_track"
        ON ("music_playlisttrack"."track_id" = "music_track"."id")
    WHERE "music_playlisttrack"."playlist_id" IN (1, 2, 3, 4)
    ORDER BY "music_playlisttrack"."position" ASC

Query 3: (inside Query 2 Prefetch) get albums for those tracks
    queryset = ....prefetch_related('track__albums', ...)

    SELECT ("music_albumtrack"."track_id") AS "_prefetch_related_val_track_id",
       "music_album"."id",
       "music_album"."name",
       "music_album"."cover",
       "music_album"."released"
    FROM "music_album"
    INNER JOIN "music_albumtrack"
        ON ("music_album"."id" = "music_albumtrack"."album_id")
    WHERE "music_albumtrack"."track_id" IN (6, 25, 39, 40, 11, 45, 29, 20, 38, 24, 42, 32, 47, 18, 2, 37)

Query 4: (inside Query 2 Prefetch) get artists for those tracks
    queryset = ......prefetch_related(..., 'track__artists')

    SELECT ("music_trackartist"."track_id") AS "_prefetch_related_val_track_id",
       "music_artist"."id",
       "music_artist"."name"
    FROM "music_artist"
    INNER JOIN "music_trackartist"
        ON ("music_artist"."id" = "music_trackartist"."artist_id")
    WHERE "music_trackartist"."track_id" IN (6, 25, 39, 40, 11, 45, 29, 20, 38, 24, 42, 32, 47, 18, 2, 37)
 
       -SQL statements from Debug tool
 """