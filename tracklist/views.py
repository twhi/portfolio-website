from django.shortcuts import render, redirect
from .forms import TracklistForm, SpotifyForm
from .tracklist import Tracklist
from .spotify import Spotify


def complete(request):

    context = {
        'found': request.session['found'],
        'total': request.session['total'],
        'complete': request.session['complete'],
        'tracklist': request.session['tracklist'],
    }
    return render(request, 'complete.html', context)


def _reduce_playlist(tl, tracks_to_keep):
    return [tl[int(i)] for i in tracks_to_keep]


def customise(request):
    sp_form = SpotifyForm()
    spotify = Spotify(request)
    sp_username = spotify.get_spotify_username()
    if request.method == 'POST':
        if 'add-to-spotify' in request.POST:
            if 'tracklist' in request.session:
                sp_form = SpotifyForm(request.POST)
                if sp_form.is_valid():

                    # get selected checkboxes
                    checkboxes = request.POST.getlist('chk')

                    # get stored tracklist
                    tracklist = request.session['tracklist']

                    # reduce tracklist based on user's checkbox selection
                    tracklist_reduced = _reduce_playlist(tracklist, checkboxes)

                    # get playlist name from form input
                    pl = sp_form.cleaned_data['playlist_name']

                    # add tracks to spotify
                    (found, total, tracklist) = spotify.add_to_spotify(tracklist_reduced, pl)

                    # store data in session variables
                    request.session['tracklist'] = tracklist_reduced
                    request.session['found'] = found
                    request.session['total'] = total
                    request.session['complete'] = True

                    return redirect('../complete/')

    context = {
        'website_name': request.session['website_name'],
        'sp_form': sp_form,
        'spotify_username': sp_username,
        'tracklist': request.session['tracklist']
    }
    return render(request, 'customise.html', context)


def connect(request):
    tl = None
    tl_form = TracklistForm()
    spotify = Spotify(request)
    sp_username = spotify.get_spotify_username()

    if request.method == 'POST':
        if 'tracklist-submit' in request.POST:
            tl_form = TracklistForm(request.POST)
            if tl_form.is_valid():
                url = tl_form.cleaned_data['url']

                try:
                    tl = Tracklist(url)
                except Exception as e:
                    if tl:
                        tl.driver.quit()
                    raise e

                if tl.raw_html:
                    print(tl.raw_html)
                    try:
                        tracklist = tl.construct_tracklist()
                        print(tracklist)
                    except Exception as e:
                        print(e)
                        tracklist = "TracklistError"

                request.session['website_name'] = tl.xpath['name']
                request.session['tracklist'] = tracklist
                return redirect('./customise/')

    context = {
        'tl_form': tl_form,
        'spotify_username': sp_username,
        'tracklist_page': 'active'
    }
    return render(request, 'tracklist.html', context)
