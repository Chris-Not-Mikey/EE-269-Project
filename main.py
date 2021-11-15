import spotipy
from client import clientID, clientSecret

from spotipy.oauth2 import SpotifyClientCredentials

cid = clientID

secret = clientSecret


client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
