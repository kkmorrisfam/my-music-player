from django.contrib import admin

# Register your models here.
from .models import (
    Artist, Album, Track, Category, TrackArtist,
    AlbumArtist, AlbumTrack, Favorite,
    PlayHistory, Playlist, PlaylistTrack
)

# Register everything so it appears in /admin
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Category)


# User-related models
admin.site.register(Favorite)
admin.site.register(PlayHistory)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)