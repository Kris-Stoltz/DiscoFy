import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Playlist:

    def __init__(self):
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id='id',
                client_secret='secret',
                redirect_uri='http://example.com',
                scope='playlist-modify-private',
                username='4wtfllm7kh9lrwhu1nitlm49i',
                cache_path='token.txt'
            )
        )
        self.songs = []

    def get_playlist(self, url):
        """ Takes in a spotify playlist URL and returns all songs in the playlist """
        playlist_id = url.split('/')[4]
        playlist = self.client.playlist_items(playlist_id)['tracks']['items']
        for item in playlist:
            song_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            title = song_name + ' - ' + artist_name
            self.songs.append(title)
