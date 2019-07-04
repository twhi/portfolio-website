from django.shortcuts import render, redirect
from .forms import TracklistForm
import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
from spotipy import oauth2
import os



# INITIALISE SPOTIFY API VARIABLES
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')
username = os.environ.get('UNAME')
scope = 'user-library-read playlist-modify-public user-read-private'
sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)













# TODO: trying to authorize user on spotify is a pain in the arsehole







def connect_to_spotify(request):
    auth_url = sp_oauth.get_authorize_url()

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print('Found cached token')
        access_token = token_info['access_token']
        print(access_token)
    else:
        print('No cached token found')

    return None

def tracklist(request):
    tracklist = None
    form = TracklistForm()
    if request.method == 'POST':
        if 'spotify-connect' in request.POST:
            print('conntecting to spotify')
            spotify = connect_to_spotify(request)
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
