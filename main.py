import spotipy
from client import clientID, clientSecret

from spotipy.oauth2 import SpotifyClientCredentials

from urllib.request import urlretrieve


cid = clientID
secret = clientSecret

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_tracks(user_id, playlist_id):
    results = sp.user_playlist_tracks(user_id, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


if __name__ == "__main__":

    #playlists = get_playlists_by_genre("monte rio skatepark", 10)

    # print_playlist_info(playlists)

    spotify_user_id = "chris_calloway"

    # Sub genre one
    subgenre_one = "shoegaze"
    spotify_playlist_one = "7lv7LjQ1dOU44Cois40DBd"

    playlist_one_tracks = get_playlist_tracks(
        spotify_user_id, spotify_playlist_one)
    preview_urls = []
    for i in playlist_one_tracks:

        if i["track"]["preview_url"] != None:
            preview_urls.append(i["track"]["preview_url"])

    directory = "./" + subgenre_one
    for j in range(len(preview_urls)):
        urlretrieve(preview_urls[j], "{}/{}{}".format(directory,
                                                      'track{}'.format(j+1), ".mp3"))

    # Sub genre two
    subgenre_two = "dreampop"
    spotify_playlist_two = "7buyfcBw6G2PoHYY65mhGW"

    playlist_two_tracks = get_playlist_tracks(
        spotify_user_id, spotify_playlist_two)
    preview_urls = []
    for z in playlist_two_tracks:

        if z["track"]["preview_url"] != None:
            preview_urls.append(z["track"]["preview_url"])

    directory = "./" + subgenre_two
    for k in range(len(preview_urls)):
        urlretrieve(preview_urls[k], "{}/{}{}".format(directory,
                                                      'track{}'.format(k+1), ".mp3"))
