import spotipy
from social_django.utils import load_strategy
import re
from fuzzywuzzy import fuzz, process

try:
    from .utils.exceptions import TracksNotFoundOnSpotifyError
except ImportError:
    from utils.exceptions import TracksNotFoundOnSpotifyError


class Spotify:
    found_count = 0

    def __init__(self, request):
        self.request = request
        self.user = self.get_authorised_user()
        self.spotipy_session = self.get_spotipy_session()

    def get_spotify_username(self):
        if self.user:
            return self.user.uid

    def get_authorised_user(self):
        try:
            u = self.request.user
            return u.social_auth.get(provider='spotify')
        except:
            return None

    def get_spotipy_session(self):
        if self.user:

            # start authenticated spotipy instance
            sp_access_token = self.user.extra_data['access_token']
            sp = spotipy.Spotify(auth=sp_access_token)

            # try a task that requires authentication if this fails then the token has expired.
            try:
                sp.user(self.get_spotify_username())
            except Exception as e:
                print(e)
                # refresh the token using load_strategy()
                strategy = load_strategy()
                self.user.refresh_token(strategy)
                sp_access_token = self.user.extra_data['access_token']
                sp = spotipy.Spotify(auth=sp_access_token)
            return sp

    @staticmethod
    def _construct_search_string(t):
        track_title = re.sub("[\(\[].*?[\)\]]", "", t['title'][0])  # REMOVE BRACKETS
        track_title = re.sub(r'([^\s\w]|_)+', '', track_title)  # REMOVE PUNCTUATION
        track_title.strip()  # REMOVE LEADING AND TRAILING WHITESPACE
        track_artists = t['artist']
        search_string = track_artists[0] + ' ' + track_title
        return search_string

    def add_to_spotify(self, tracklist, playlist_name):

        # generate a list of spotify track IDs
        found_list = []
        for t in tracklist:
            search_string = self._construct_search_string(t)
            results = self.spotipy_session.search(q=search_string, limit=10)
            track_id = self._get_track_id_from_search_results(results, t)
            found_list.append(track_id)

        # if no tracks are found then throw error
        if found_list.count(False) == len(found_list):
            raise TracksNotFoundOnSpotifyError()

        # get/create playlist
        playlist = self.playlist_exists(playlist_name)
        if not playlist:
            playlist = self.create_playlist(playlist_name)

        # add tracks to playlist
        for t, track_id in zip(tracklist, found_list):
            found = self._add_to_playlist(playlist['id'], track_id)
            self.found_count += found

            if found == 1:
                t['found'] = True
            else:
                t['found'] = False

        return {
            'found': self.found_count,
            'total': len(tracklist),
            'tracklist': tracklist,
            'playlist_link': playlist['external_urls']['spotify'],
        }

    def _add_to_playlist(self, playlist_id, track_id):
        if track_id:
            self.spotipy_session.user_playlist_add_tracks(user=self.get_spotify_username(), playlist_id=playlist_id,
                                                          tracks=track_id)
            return 1
        else:
            return 0

    def playlist_exists(self, name):
        existing_playlists = self.spotipy_session.user_playlists(self.get_spotify_username())['items']
        for playlist in existing_playlists:
            if name in playlist['name']:
                return playlist
        return False

    def create_playlist(self, name):
        return self.spotipy_session.user_playlist_create(self.get_spotify_username(), name=name, public=True)

    @staticmethod
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


class SpotifyTest:
    found_count = 0

    def __init__(self, spotipy_session, username):
        self.spotipy_session = spotipy_session
        self.username = username

    @staticmethod
    def _construct_search_string(t):
        track_title = re.sub("[\(\[].*?[\)\]]", "", t['title'][0])  # REMOVE BRACKETS
        track_title = re.sub(r'([^\s\w]|_)+', '', track_title)  # REMOVE PUNCTUATION
        track_title.strip()  # REMOVE LEADING AND TRAILING WHITESPACE
        track_artists = t['artist']
        search_string = track_artists[0] + ' ' + track_title
        return search_string

    def add_to_spotify(self, tracklist, playlist_name):
        # generate a list of spotify track IDs
        found_list = []
        for t in tracklist:
            search_string = self._construct_search_string(t)
            results = self.spotipy_session.search(q=search_string, limit=10)
            track_id = self._get_track_id_from_search_results(results, t)
            found_list.append(track_id)

        # if no tracks are found then throw error
        if found_list.count(False) == len(found_list):
            raise TracksNotFoundOnSpotifyError()

        # get/create playlist
        playlist = self.playlist_exists(playlist_name)
        if not playlist:
            playlist = self.create_playlist(playlist_name)

        # add tracks to playlist
        for track_id in found_list:
            found = self._add_to_playlist(playlist['id'], track_id)
            self.found_count += found

            if found == 1:
                t['found'] = True
            else:
                t['found'] = False

        return {
            'found': self.found_count,
            'total': len(tracklist),
            'tracklist': tracklist,
            'playlist_link': playlist['external_urls']['spotify'],
        }

    def _add_to_playlist(self, playlist_id, track_id):
        if track_id:
            self.spotipy_session.user_playlist_add_tracks(user=self.username, playlist_id=playlist_id, tracks=track_id)
            return 1
        else:
            return 0

    @property
    def playlist_link(self):
        return 'https://open.spotify.com/playlist/{}'.format('3434f')

    def playlist_exists(self, name):
        existing_playlists = self.spotipy_session.user_playlists(self.username)['items']
        for playlist in existing_playlists:
            if name in playlist['name']:
                return playlist
        return False

    def create_playlist(self, name):
        return self.spotipy_session.user_playlist_create(self.username, name=name, public=True)

    @staticmethod
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


if __name__ == '__main__':
    import os
    import spotipy.util as util
    from tracklist import Tracklist

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_uri = os.environ.get('REDIRECT_URI')
    username = os.environ.get('UNAME')
    scope = 'user-library-read playlist-modify-public user-read-private'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        url = 'https://www.nts.live/shows/budgie/episodes/budgie-01-08-2019'
        tl = Tracklist(url)
        tracklist = tl.construct_tracklist()
        #
        sp = SpotifyTest(sp, username)
        sp.add_to_spotify(tracklist, 'sp test')
