from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TracklistForm, SpotifyForm
from .tracklist import Tracklist
from .spotify import Spotify
from .utils.exceptions import WebsiteNotSupportedError, InvalidUrlError, NoTracklistError, TracksNotFoundOnSpotifyError


def complete(request):
    context = {
        'found': request.session['found'],
        'total': request.session['total'],
        'complete': request.session['complete'],
        'playlist_link': request.session['playlist_link'],
        'tracklist': request.session['tracklist_reduced'],
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
                    try:
                        results = spotify.add_to_spotify(tracklist_reduced, pl)
                    except TracksNotFoundOnSpotifyError:
                        messages.error(request,
                                       "Couldn't find any of tracks for this show on Spotify.", "danger")
                        return redirect('../')

                    # store data in session variables
                    request.session['tracklist_reduced'] = tracklist_reduced
                    request.session['found'] = results['found']
                    print(tracklist_reduced)
                    request.session['total'] = results['total']
                    request.session['playlist_link'] = results['playlist_link']
                    request.session['complete'] = True

                    return redirect('../complete/')
            else:
                return redirect('../')

    context = {
        'website_name': request.session['website_name'],
        'sp_form': sp_form,
        'spotify_username': sp_username,
        'tracklist': request.session['tracklist']
    }
    return render(request, 'customise.html', context)


def connect(request):
    tracklist = None
    tl = None
    tl_form = TracklistForm()
    spotify = Spotify(request)
    sp_username = spotify.get_spotify_username()

    if request.method == 'POST':
        if 'tracklist-submit' in request.POST:
            tl_form = TracklistForm(request.POST)
            if tl_form.is_valid():
                url = tl_form.cleaned_data['url']

                # get tracklist from web and error catching
                try:
                    tl = Tracklist(url)
                except InvalidUrlError as e:
                    if tl:
                        tl.driver.quit()
                    messages.error(request,
                                   "Unable to connect to URL. Is your URL valid? Attempted to access {}".format(e),
                                   "danger")
                    return redirect(request.path_info)
                except WebsiteNotSupportedError as e:
                    if tl:
                        tl.driver.quit()
                    messages.error(request, "Website not supported. Attempted to access {}".format(e), "danger")
                    return redirect(request.path_info)
                except Exception as e:
                    if tl:
                        tl.driver.quit()
                    messages.error(request, "An unknown error has occured. {}".format(e), "danger")
                    return redirect(request.path_info)

                # construct tracklist and error catching
                try:
                    tracklist = tl.construct_tracklist()
                except NoTracklistError as e:
                    messages.error(request,
                                   "Unable to find a tracklist at specified URL. Attempted to access {}".format(e),
                                   "danger")
                    return redirect(request.path_info)
                except Exception as e:
                    messages.error(request, "An unknown error has occured. {}".format(e), "danger")
                    return redirect(request.path_info)

                request.session['website_name'] = tl.xpath['name']
                request.session['tracklist'] = tracklist
                return redirect('./customise/')

    context = {
        'tl_form': tl_form,
        'spotify_username': sp_username,
        'tracklist_page': 'active'
    }
    return render(request, 'tracklist.html', context)
