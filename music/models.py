from django.db import models


# Create your models here.

class Track(models.Model):
    title = models.CharField(max_length=200)
    audio = models.FileField(upload_to='tracks/', max_length=100)   
    artists = models.ManyToManyField("Artist", through="TrackArtist" ,related_name="tracks", blank=True)
    albums = models.ManyToManyField("Album", through="AlbumTrack", related_name="tracks", blank=True)
    categories = models.ManyToManyField("Category", related_name="tracks", blank=True) # django creates simple join table without defining class for "through"

    def __str__(self):
        return self.title

class Album(models.Model):
    name = models.CharField(max_length=100)
    cover = models.FileField(
        upload_to='album_img/', 
        default="album_img/fallback.webp",
        max_length=100)
    artists = models.ManyToManyField("Artist", through="AlbumArtist", related_name="albums", blank=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Join/Through tables for Many-to-Many relationships

class TrackArtist(models.Model):
    # create enum type choices.  Is artist Primary artist or Featured (guest) artist on track?
    # add other roles later like, writer, producer, etc.
    class Role(models.TextChoices):
        PRIMARY  = "primary",  "Primary"
        FEATURED = "featured", "Featured"
        
    track = models.ForeignKey("Track", on_delete=models.CASCADE) # if parent Track is deleted, then join row will be deleted
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PRIMARY)
    order = models.PositiveSmallIntegerField(default=0)


    class Meta:
        unique_together = [("track", "artist")]  # can only have one combination for artist and track, not handling different recordings of same song
        ordering = ["order", "id"]

# For when there is more than one artist on an album, like a Christmas compilation
class AlbumArtist(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [("album", "artist")]
        ordering = ["order", "id"]

class AlbumTrack(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    track = models.ForeignKey("Track", on_delete=models.CASCADE)
    track_number = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        unique_together = [("album", "track")]
        ordering = ["track_number", "id"]

