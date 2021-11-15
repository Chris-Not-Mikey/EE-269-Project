import spotipy
from client import clientID, clientSecret

from spotipy.oauth2 import SpotifyClientCredentials

from urllib.request import urlretrieve


cid = clientID

secret = clientSecret


client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# for i in range(0, 1000, 50):

#     track_results = sp.search(q="dream pop", type="track", limit=50, offset=i)

#     for i, t in enumerate(track_results["tracks"]["items"]):
#         print(t['artists'][0]['name'])


lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
results = sp.artist_top_tracks(lz_uri)

preview_urls = []

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    preview_urls.append(track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()


directory = "./"

for i in range(len(preview_urls)):
    urlretrieve(preview_urls[i], "{}/{}{}".format('./',
                                                  'track{}'.format(i+1), ".mp3"))
