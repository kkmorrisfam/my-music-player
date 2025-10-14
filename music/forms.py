from django import forms
# from django.forms.widgets import HiddenInput
from . import models

class AddPlaylistForm(forms.ModelForm):
    class Meta:
        model = models.Playlist
        fields = ['name']