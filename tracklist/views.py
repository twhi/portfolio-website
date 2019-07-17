from django.shortcuts import render
from .forms import TracklistForm, SpotifyForm
from .tracklist import Tracklist
from .spotify import Spotify


def tracklist(request):
    found = None
    total = None
    tracklist = None
    pl = None
    complete = False

    tl_form = TracklistForm()
    sp_form = SpotifyForm()
    spotify = Spotify(request)
    sp_username = spotify.get_spotify_username()
    sp = spotify.get_spotipy_session()

    if request.method == 'POST':
        print('post request detected')
        if 'tracklist-submit' in request.POST:
            tl_form = TracklistForm(request.POST)
            if tl_form.is_valid():
                url = tl_form.cleaned_data['url']
                tl = Tracklist(url)
                if tl.raw_html:
                    tracklist = tl.construct_tracklist()
                request.session['tracklist'] = tracklist

        elif 'add-to-spotify' in request.POST:
            print('adding tracks to spotify')
            if 'tracklist' in request.session:
                sp_form = SpotifyForm(request.POST)
                if sp_form.is_valid():
                    tracklist = request.session['tracklist']
                    pl = sp_form.cleaned_data['playlist_name']
                    (found, total, tracklist) = spotify.add_to_spotify(tracklist, pl)
                    complete = True

    context = {
        'tl_form': tl_form,
        'sp_form': sp_form,
        'tracklist': tracklist,
        'spotify_username': sp_username,
        'user_playlists': pl,
        'found': found,
        'total': total,
        'complete': complete,
        'tracklist_page': 'active'
    }
    return render(request, 'tracklist.html', context)
