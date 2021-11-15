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

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     preview_urls.append(track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()


def get_playlists_by_genre(genre, limit):
    results = sp.search(genre, limit=limit, type='playlist')
    return results['playlists']['items']


def print_playlist_info(playlists):
    for playlist in playlists:
        # print(playlist)
        print('{}: {}'.format(
            playlist['name'],
            '{} tracks'.format(playlist['tracks']['total']))



        )


def get_playlist_tracks(user_id, playlist_id):
    results = sp.user_playlist_tracks(user_id, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_playlist_songs(playlist):

    for playlist in playlists:
        print(playlist["tracks"]["href"])

        ply_uri = playlist["tracks"]["href"]

        result = sp.playlist(ply_uri)

        print(result)

        # for track in playlist['tracks']:
        #     print('track    : ' + track['name'])
        #     print('audio    : ' + track['preview_url'])
        #     preview_urls.append(track['preview_url'])
        #     print('cover art: ' + track['album']['images'][0]['url'])
        #     print()
        # directory = "./"
        # for i in range(len(preview_urls)):
        #     urlretrieve(preview_urls[i], "{}/{}{}".format('./',
        #                                                   'track{}'.format(i+1), ".mp3"))
if __name__ == "__main__":

    print('here')
    playlists = get_playlists_by_genre("monte rio skatepark", 10)

    print_playlist_info(playlists)

    # get_playlist_songs(playlists)

    tracks = get_playlist_tracks(
        "chris_calloway", "7lv7LjQ1dOU44Cois40DBd")

    counter = 0
    for i in tracks:

        print(i["track"]["name"])
        print(i["track"]["preview_url"])

        if i["track"]["preview_url"] != None:
            preview_urls.append(i["track"]["preview_url"])

        counter = counter + 1

    directory = "./tracks"
    for j in range(len(preview_urls)):
        urlretrieve(preview_urls[j], "{}/{}{}".format('./',
                                                      'track{}'.format(j+1), ".mp3"))
