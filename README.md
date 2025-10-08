# My Music App

## Overview

I've created a music app in Django and connected it to a PostgreSQL database.  The database uses a normalized design which uses many-to-many relationships for data retrieval. I've added my own css file for styling and added html templates.  

The models are set up so that an album can have multiple tracks, one artist or multiple artists.  However if you display an album with the artist and there are many artists, it will just display “various” for the artist field.  A track can be listed on multiple albums and an artist can be on both an album and a track.  A track can also have multiple artists. At this point I have not utilized everything I can with this design, but would like it to be flexible as I add to it in the future.

The purpose of this app was to become familiar with audio files and data retrieval so that I could work on creating a podcast app in the future.

## Web Pages

Library (Home):
When users land on the Home page, they see the title “Music Library” a “Check out my playlists” link. The navbar is consistent across the site (Logo, Library, Playlists, About).  In the main section of the page are cards with all of the music tracks in the library.  The cards display the Album cover, the track name and the artist or artists.  The card also includes an audio link so that a user can play the audio for that track.

Playlists:
This page displays playlists unique to the user. It displays cards similar to the library page, but it displays the album image from the first track in the playlist, the playlist title and the first two artists from the tracks in the playlist.  When a user clicks anywhere on the playlist card, it takes the user to the playlist detail page.  It passes the primary key of the playlist to the playlist view page to display one playlist.

Playlist Detail:
This page displays the details for the playlist chosen on the playlists page.  The album cover for the first track is displayed prominently, then beneath, a list of song titles with their artists, and a link to the audio file. A user can then choose and play a music track.

About Page:
This page displays details for images and audio copyright information for assets used in this project.

## Development Environment

I used VSCode on a Windows machine to develop this software.  I utilized a virtual environment “venv”. These are the commands I used.

Create venv environment

```powershell
py -m venv .venv
```

You have to activate the virtual environment whenever you open a new terminal window.

Start venv environment (on windows)

```powershell
.\.venv\Scripts\Activate.ps1
```

Stop venv environment

```powershell
deactivate
```

After I started the venv environment, then I installed Django and my packages. I installed Django

```powershell
py -m pip install Django
```

Packages installed are found in the requirements.txt project file and include:

* Pillow
* Django debug toolbar
* Django stubs
* Psycopg2

## Useful Websites

* [django documentation](https://www.djangoproject.com/)
* [Real Python](https://realpython.com/python-virtual-environments-a-primer/)
* [Python.org Documentation](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
* [HTMX Documentation](https://htmx.org/docs/)

## Future Work

* Add user registration and login functionality
* If user is logged in, a user can add a track to their playlist
* Setup app in the cloud for production, with a cloud database
* Add form to upload user albums or songs
