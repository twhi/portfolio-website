from django.shortcuts import render
from .forms import TracklistForm, SpotifyForm
import requests
from bs4 import BeautifulSoup
import spotipy
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def get_authorised_user(r):
    try:
        user = r.user
        return user.social_auth.get(provider='spotify')
    except:
        return None


def get_user_playlists(sp, username):
    pl = sp.user_playlists(username)['items']
    playlists = []
    for p in pl:
        playlists.append(p['name'])
    return playlists


def _construct_search_string(track):
    track_title = re.sub("[\(\[].*?[\)\]]", "", track['title'])  # REMOVE BRACKETS
    track_title = re.sub(r'([^\s\w]|_)+', '', track_title)  # REMOVE PUNCTUATION
    track_title.strip()  # REMOVE LEADING AND TRAILING WHITESPACE
    track_artists = track['artist']
    search_string = track_artists[0] + ' ' + track_title
    return search_string


def _get_track_id_from_search_results(results, track):
    track_artists = track['artist']
    for result in results['tracks']['items']:
        result_artists = result['artists']
        result_artists_combined = [''.join(x['name'].lower()) for x in result_artists]
        best_result = process.extractOne(track_artists[0].lower().strip(), result_artists_combined,
                                         scorer=fuzz.ratio)
        score = best_result[1]
        if score > 90:
            track_id = [result['id']]
            return track_id
    return False


def _add_to_playlist(sp, un, playlist_id, track_id):
    if track_id:
        sp.user_playlist_add_tracks(user=un, playlist_id=playlist_id, tracks=track_id)
        return True
    else:
        return False


def add_to_spotify(sp, tl, pl, un):
    print('adding track to spotify playlist', pl)
    playlist_id = _make_playlist(sp, pl, un)
    for track in tl:
        search_string = _construct_search_string(track)
        results = sp.search(q=search_string, limit=10)
        track_id = _get_track_id_from_search_results(results, track)
        _add_to_playlist(sp, un, playlist_id, track_id)


def _make_playlist(sp, pl, un):
    playlist_exists = False
    existing_playlists = sp.user_playlists(un)['items']
    for playlist in existing_playlists:
        print(playlist['name'])
        if pl in playlist['name']:
            playlist_exists = True
            playlist_id = playlist['id']
            break
    if not playlist_exists:
        playlist = sp.user_playlist_create(un, name=pl, public=True)
        playlist_id = playlist['id']
    return playlist_id


def tracklist(request):
    sp_username = None
    tracklist = None
    pl = None
    sp_form = None

    user = get_authorised_user(request)
    if user:
        # start authenticated spotipy instance
        sp_access_token = user.extra_data['access_token']
        sp = spotipy.Spotify(auth=sp_access_token)

        # get user's playlists
        sp_username = user.uid
        pl = get_user_playlists(sp, sp_username)

    tl_form = TracklistForm()
    sp_form = SpotifyForm()
    if request.method == 'POST':
        print('post request detected')
        if 'tracklist-submit' in request.POST:
            tl_form = TracklistForm(request.POST)
            if tl_form.is_valid():
                url = tl_form.cleaned_data['url']
                tracklist = get_data(url)
                request.session['tracklist'] = tracklist

        elif 'add-to-spotify' in request.POST:
            print('adding tracks to spotify')
            if 'tracklist' in request.session:
                sp_form = SpotifyForm(request.POST)
                if sp_form.is_valid():
                    tl = request.session['tracklist']
                    pl = sp_form.cleaned_data['playlist_name']
                    add_to_spotify(sp, tl, pl, sp_username)

    context = {
        'tl_form': tl_form,
        'sp_form': sp_form,
        'tracklist': tracklist,
        'spotify_username': sp_username,
        'user_playlists': pl,
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
