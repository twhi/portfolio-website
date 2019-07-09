from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import TracklistForm
import requests
from bs4 import BeautifulSoup


def tracklist(request):
    user = User.objects.all()[0]
    social = user.social_auth.get(provider='spotify')
    sp_username = social.uid
    sp_access_token = social.extra_data['access_token']
    tracklist = None
    form = TracklistForm()
    if request.method == 'POST':
        # if 'spotify-connect' in request.POST:
        #     print('conntecting to spotify')
        #     # spotify = connect_to_spotify(request)
        form = TracklistForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            tracklist = get_data(url)
    context = {
        'form': form,
        'tracklist': tracklist,
        'tracklist_page': 'active'
    }
    return render(request, 'tracklist.html', context)


def get_data(url):
    tracklist_html = get_tracklist_from_url(url)
    artist_list = get_artists_from_html(tracklist_html)
    track_list = get_tracks_from_html(tracklist_html)
    setlist = contruct_setlist(track_list, artist_list)
    return setlist


def get_tracklist_from_url(url):
    session = requests.Session()
    raw_html = session.get(url).text
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.findAll('li', {'class': 'track'})


def get_artists_from_html(tracklist_html):
    artist_list = []
    for track in tracklist_html:
        artist_name_list = track.findAll('span', {'class': 'track__artist'})
        current_list = []
        for artist in artist_name_list:
            if artist.text not in current_list:
                current_list.append(artist.text)
        artist_list.append(current_list)
    return artist_list


def get_tracks_from_html(tracklist_html):
    track_list = []
    for track in tracklist_html:
        track_name = track.find('span', {'class': 'track__title'}).text
        track_list.append(track_name)
    return track_list


def contruct_setlist(track_list, artist_list):
    setlist = []
    for track, artist in zip(track_list, artist_list):
        current_item = {'artist': artist, 'title': track}
        setlist.append(current_item)
    return setlist
