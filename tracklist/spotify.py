import spotipy
from social_django.utils import load_strategy
import re
from fuzzywuzzy import fuzz, process

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
                sp.user(self.spotify_username)
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
        playlist_id = self.playlist_exists(playlist_name)
        if not playlist_id:
            playlist_id = self.create_playlist(playlist_name)

        for t in tracklist:
            search_string = self._construct_search_string(t)
            results = self.spotipy_session.search(q=search_string, limit=10)
            track_id = self._get_track_id_from_search_results(results, t)
            found = self._add_to_playlist(playlist_id, track_id)
            self.found_count += found

            if found == 1:
                t['found'] = True
            else:
                t['found'] = False

        return self.found_count, len(tracklist), tracklist

    def _add_to_playlist(self, playlist_id, track_id):
        if track_id:
            self.spotipy_session.user_playlist_add_tracks(user=self.get_spotify_username(), playlist_id=playlist_id, tracks=track_id)
            return 1
        else:
            return 0


    def playlist_exists(self, name):
        existing_playlists = self.spotipy_session.user_playlists(self.get_spotify_username())['items']
        for playlist in existing_playlists:
            if name in playlist['name']:
                return playlist['id']
        return False

    def create_playlist(self, name):
        playlist = self.spotipy_session.user_playlist_create(self.get_spotify_username(), name=name, public=True)
        playlist_id = playlist['id']
        return playlist_id

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

