import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unicodedata

def get_spotify_url(artist: str, song_name: str, album: str):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "0285e2a6aa6047e3bc755c457ef19423" , client_secret = "6192d0ffeb354e6ab751bac2018f07e2"))
        print("in")
        results = sp.search(q = unicodedata.normalize("NFKD", f"{song_name}&album:{album}&artist:{artist}"), limit=5)
        print(results)
        return results['tracks']['items'][0]['external_urls']['spotify']


print(get_spotify_url("The Weeknd", "Alone Again", "After Hours"))
