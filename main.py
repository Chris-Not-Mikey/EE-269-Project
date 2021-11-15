import spotipy
from client import clientID, clientSecret

from spotipy.oauth2 import SpotifyClientCredentials

from urllib.request import urlretrieve

from create_database import make_audio_data_array, train_test_split
import numpy as np

full_path = "/Users/chris/Desktop/Fall-2021/Signal Processing/EE-269-Project/"
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

    # playlists = get_playlists_by_genre("monte rio skatepark", 10)

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

    directory_one = full_path + subgenre_one
    # for j in range(len(preview_urls)):
    #     urlretrieve(preview_urls[j], "{}/{}{}".format(directory_one,
    #                                                   'track{}'.format(j+1), ".mp3"))

    # Sub genre two
    subgenre_two = "dreampop"
    spotify_playlist_two = "7buyfcBw6G2PoHYY65mhGW"

    playlist_two_tracks = get_playlist_tracks(
        spotify_user_id, spotify_playlist_two)
    preview_urls = []
    for z in playlist_two_tracks:

        if z["track"]["preview_url"] != None:
            preview_urls.append(z["track"]["preview_url"])

    directory_two = full_path + subgenre_two
    # for k in range(len(preview_urls)):
    #     urlretrieve(preview_urls[k], "{}/{}{}".format(directory_two,
    #                                                   'track{}'.format(k+1), ".mp3"))

    # Get Data for genre one
    raw_genre_one_data, sr = make_audio_data_array(directory_two)
    print(directory_two)

    # split into training and testing data
    genre_one_train, genre_one_test = train_test_split(raw_genre_one_data, 1)

    # Save data
    genre_one_train_folder = full_path + "/genre_one_train/genre_one_train"
    genre_one_test_folder = full_path + "/genre_one_test/genre_one_test"
    np.save(genre_one_train_folder, genre_one_train)
    np.save(genre_one_test_folder, genre_one_test)

    # Get Data for genre two
    raw_genre_two_data, sr = make_audio_data_array(directory_one)
    print(directory_one)

    # split into training and testing data
    genre_two_train, genre_two_test = train_test_split(raw_genre_two_data, 1)

    # Save data
    genre_two_train_folder = full_path + "/genre_two_train/genre_two_train"
    genre_two_test_folder = full_path + "/genre_two_test/genre_two_test"
    np.save(genre_two_train_folder, genre_two_train)
    np.save(genre_two_test_folder, genre_two_test)
