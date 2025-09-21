from django.contrib import admin
from .models import (
    Artist, Album, Track, Category, TrackArtist,
    AlbumArtist, AlbumTrack, Favorite,
    PlayHistory, Playlist, PlaylistTrack
)

# The admin interface has the ability to edit models on the same page 
# as a parent model. These are called inlines.
# add join tables on parent forms
class AlbumTrackInline(admin.TabularInline):
    model = AlbumTrack
    extra = 1   # show 1 empty row by default

class TrackArtistInline(admin.TabularInline):
    model = TrackArtist
    extra = 1

class AlbumArtistInline(admin.TabularInline):
    model = AlbumArtist
    extra = 1


# Register your models here.

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AlbumArtistInline, AlbumTrackInline]

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TrackArtistInline]
    filter_horizontal = ("categories",) 

admin.site.register(Artist)
#admin.site.register(Album)
#admin.site.register(Track)
admin.site.register(Category)


# User-related models
admin.site.register(Favorite)
admin.site.register(PlayHistory)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)

# join tables
admin.site.register(TrackArtist)
admin.site.register(AlbumArtist)
admin.site.register(AlbumTrack)