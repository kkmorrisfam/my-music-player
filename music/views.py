from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Track, Artist, Playlist, PlaylistTrack
from django.db.models.functions import Random
from django.db.models import Prefetch, Q, Max
from django.contrib.auth.decorators import login_required
from .forms import AddPlaylistForm
from django.db import IntegrityError, transaction, DatabaseError
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from django.contrib import messages

# function to query database for user playlists
def _user_playlists(user):
    # pt_qs = (PlaylistTrack.objects
    #          .select_related("track")
    #          .prefetch_related("track__albums", "track__artists")
    #          .order_by("position", "id"))
    # return (Playlist.objects
    #         .filter(owner=user)
    #         .prefetch_related(Prefetch("playlisttrack_set", queryset=pt_qs, to_attr="pt_items")))

    prefetch = Prefetch("playlisttrack_set", queryset=(
                        PlaylistTrack.objects
                        .select_related('track')
                        .prefetch_related('track__albums','track__artists')
                        .order_by('position')
                        ), to_attr='pt_items'
               )
    return (Playlist.objects
                            .filter(owner=user)
                            .prefetch_related(prefetch))

# function to query database for Playlist data
def get_playlist_for_display(user, pk: int) -> Playlist:
    prefetch = Prefetch(
                        'playlisttrack_set', 
                        queryset=(
                            PlaylistTrack.objects
                            .select_related('track')
                            .prefetch_related('track__albums', 'track__artists')
                            .order_by('position', 'id')                            
                        ), to_attr='items'
    )
    
    
    return get_object_or_404(
                        Playlist.objects.
                        select_related("owner")                     
                        .prefetch_related(prefetch),
                        pk=pk,
                        owner=user
                        )




# remove a playlist - I will need to remove name and tracks associated with it
@login_required
def remove_playlist(request, pk:int):
    # verify ownership and get playlist wanting to remove
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
         
    
    try:
        with transaction.atomic():
            name = playlist.name

            #Delete the one playlist
            playlist.delete()
        messages.success(request, f"Deleted playlist “{name}”.")
       
    except DatabaseError:
        messages.error(request, "Sorry—couldn’t delete that playlist. Please try again.")
        if request.headers.get("HX-Request"):
            # Re-render list even on error so the page stays consistent;            
            playlists = Playlist.objects.filter(owner=request.user).prefetch_related("tracks")
            return render(request, "music/partials/_playlists.html", {"playlists": playlists}, status=400)
        
        # If delete failed, fall back to 'next' if present, otherwise go back to the view page
        return redirect(request.POST.get("next"))
    
    if request.headers.get("HX-Request"):
        # playlists = Playlist.objects.filter(owner=request.user).prefetch_related("tracks")
        playlists = _user_playlists(request.user)
        
        # (Playlist.objects
        #          .filter(owner=request.user)
        #          .prefetch_related(Prefetch("pt_items", queryset=pt_qs)))

        return render(request, "music/partials/_playlists.html", {"playlists": playlists})

    # messages.success(request, "Playlist deleted.")
    return redirect(request.POST.get("next") or "music:playlist")



@login_required
@require_http_methods(["POST"])
@transaction.atomic
def playlist_remove_track(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)

    track_id = request.POST.get("track_id")
    if not track_id:
        return HttpResponseBadRequest("Missing track_id")
    
    track = get_object_or_404(Track, pk=track_id)

    #Delete the one row/track
    PlaylistTrack.objects.filter(playlist=playlist, track=track).delete()

    #re number positions
    items = (PlaylistTrack.objects
             .filter(playlist=playlist)
             .order_by("position", "id"))
    for idx, pt in enumerate(items, start=1):
        if pt.position != idx:
            pt.position = idx
            pt.save(update_fields=["position"])

    #return updated list
    playlist = get_playlist_for_display(request.user, pk)
    return render(request, "music/partials/_playlist_items.html", {"playlist": playlist})


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def playlist_add_track(request, pk):
    # add track to the playlist, return updated list partial
    #check ownership
    playlist = get_object_or_404(Playlist, pk=pk, owner = request.user)

    # validate
    track_id = request.POST.get("track_id")
    if not track_id:
        return render(
            request, 
            "music/partials/_playlist_items.html",
            {"playlist": get_playlist_for_display(request.user, pk)},
            status=400,
        )
    
    track = get_object_or_404(Track, pk=track_id)

    # figure out next position
    # last = PlaylistTrack.objects.filter(playlist=playlist).order_by("-position").first()
    # next_pos = (last.position + 1) if last else 1
    next_pos = (PlaylistTrack.objects.filter(playlist=playlist). aggregate(m=Max("position"))["m"] or 0) + 1

    # insert into database
    pt, created = PlaylistTrack.objects.get_or_create(
        playlist=playlist, 
        track=track,
        defaults={"position": next_pos},
    )
    
    if not created:
        pt.position = next_pos
        pt.save(update_fields=["position"])

    #render updated list partial
    playlist = get_playlist_for_display(request.user, pk)
    return render(request, "music/partials/_playlist_items.html", {"playlist" : playlist})


@login_required
def track_search(request, pk):
    # make sure playlist is owned by user
    get_object_or_404(Playlist, pk=pk, owner=request.user)

    # read query in request object url (?q=...)
    q = (request.GET.get("q") or "").strip()

    results = []
    if q:
        # if query, then build a case-insensitive filter
        # match track title or any artist name
        results = (
            Track.objects
            .filter(Q(title__icontains=q) | Q(artists__name__icontains=q))
            .distinct()  # for M2M joins, collapse filter to unique tracks
            .prefetch_related("artists")
            .order_by("title")[:25]
        )

    # render the results in the partial
    return render (request, "music/partials/_track_results.html", 
                   {"playlist_id":pk, "results":results, "q": q})    


@login_required
def playlist_items(request, pk):
    # HTMX partial that renders the album cover + tracks list
    playlist = get_playlist_for_display(request.user, pk)
    return render(request, "music/partials/_playlist_items.html", {"playlist": playlist})

# returns the composer UI (searchbar + results + current items list)
@login_required
def playlist_composer(request, pk):
    playlist = get_playlist_for_display(request.user, pk)
    return render(request, "music/partials/_playlist_composer.html", {"playlist": playlist})


# Get all Playlists for one user
#This view checks if a user is logged in, takes the primary key from the url passed in and returns
# a playlist object with all of it's tracks, the album covers and the artists associated with those tracks
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
    
    return render(request, 'music/playlist_view.html', {"playlist": playlist})


# Get data object with all tracks, with album and artists 
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




# Returns a static page "about" with no queries
def about(request):
    return render(request, 'about.html')
    # knows where it's found because of entry in the settings.py with 'DIRS'
    # 'DIRS': [BASE_DIR / 'templates'],


# Create new playlist
# if not logged in, redirects to login page
@login_required(login_url="/users/login/")
def playlist_new(request):
    if request.method == "POST":
        # create a form instance and add data from request
        form = AddPlaylistForm(request.POST)
        # see if it's valid
        if form.is_valid():
            # process the data
            # create instance of model before saving it
            new = form.save(commit=False)
            # get user, add to instance
            new.owner = request.user           
            #after getting user, try to save with user and name
            try: 
                # save instance
                new.save()
            except IntegrityError:
                form.add_error('name', 'You already have a playlist with this name.')
                #return bound form so user can see errors
                return render(request, 'music/playlist_new.html', {'form': form})
               

             # if HTMX request, return composer partial
            if request.headers.get("HX-Request") == "true":
                return playlist_composer(request, new.pk)            
            # redirect - if not htmx
            return redirect('music:playlist_view', pk=new.pk)
        
        # invalid form, rerender with errors.  Because of partials, add this here, so whole page isn't rerendered into target
        return render(request, "music/playlist_new.html", {"form": form})
    
    else:
        # create new blank instance for user to fill out
        form = AddPlaylistForm()
    #re render page with form instance        
    return render(request, 'music/playlist_new.html', {'form': form})



# Gel all playlists
# explanation for this query - below code block
# if not logged in - go to login page
@login_required(login_url="/users/login/")
def playlist(request):
    # prefetch = Prefetch("playlisttrack_set", queryset=(
    #                     PlaylistTrack.objects
    #                     .select_related('track')
    #                     .prefetch_related('track__albums','track__artists')
    #                     .order_by('position')
    #                     ), to_attr='pt_items'
    #            )
    
    # playlists = Playlist.objects.none() #if not logged in, stays as none


    # if request.user.is_authenticated:
    #     playlists = Playlist.objects.filter(owner=request.user).prefetch_related(prefetch) 

    playlists = _user_playlists(request.user)   
    return render(request, 'music/playlist.html', {"playlists": playlists})



"""  
    Explanation of query in query for get all playlists

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