from django import forms
# from django.forms.widgets import HiddenInput
from . import models
# class AddPlaylistForm(forms.Form):
#     name = forms.CharField(label="Playlist name", max_length=200)
#     created_at = forms.DateTimeField(widget=HiddenInput(), required=False)

class AddPlaylistForm(forms.ModelForm):
    class Meta:
        model = models.Playlist
        fields = ['name']