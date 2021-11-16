import spotipy
from client import clientID, clientSecret
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlretrieve
from create_database import make_audio_data_array, train_test_split
import numpy as np
import os


############################################# TO RUN ON ANOTHER SYSTEM, CHANGE THE FOLLOWING ########################################

# Path to data folders

full_path = "/Users/chris/Desktop/Fall-2021/Signal Processing/EE-269-Project/"

# Client/ClientSecret -> Need to get these by applying to spotify API. Chris's keys should work everyone for this projext
cid = clientID
secret = clientSecret

############################################# END RUN ON ANOTHER SYSTEM  ############################################################

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

    ############################################# TO CHANGE SUBGENRE, CHANGE THE FOLLOWING ########################################

    # USER_ID: Change this to the owner of the playlist (should just be user name)
    spotify_user_id = "chris_calloway"

    # Give Subgenre one a string name
    subgenre_one = "shoegaze"

    # Get Playlist ID of specific playlist: https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html
    spotify_playlist_one = "7lv7LjQ1dOU44Cois40DBd"

    # Give Subgenre two a string name
    subgenre_two = "dreampop"

    # Get Playlist ID of specific playlist: https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html
    spotify_playlist_two = "7buyfcBw6G2PoHYY65mhGW"

    # The max number of songs from the playlist that we will take. Probably don't need to touch this, but just in case it is here
    # IF you are running this on your personal computer, you may want to reduce this so you don't download 1000+ songs
    limit = 10

    ############################################# END CHANGE SUBGENRE  #############################################################

    # GET PREVIEW URLS FOR SUBGENRE 1

    playlist_one_tracks = get_playlist_tracks(
        spotify_user_id, spotify_playlist_one)
    preview_urls = []
    subgenre_one_features = []
    lf = 0
    for i in playlist_one_tracks:

        if i["track"]["preview_url"] != None and lf < limit:
            preview_urls.append(i["track"]["preview_url"])

            track_uri = i["track"]["uri"]

            features = sp.audio_features(track_uri)[0]

            # Example feature: {'danceability': 0.612, 'energy': 0.476, 'key': 8, 'loudness': -8.256, 'mode': 1, 'speechiness': 0.0275, 'acousticness': 0.861, 'instrumentalness': 0.0044, 'liveness': 0.147, 'valence': 0.257, 'tempo': 118.381, 'type': 'audio_features', 'id': '6asU049doNupkVllo61luh', 'uri': 'spotify:track:6asU049doNupkVllo61luh', 'track_href': 'https://api.spotify.com/v1/tracks/6asU049doNupkVllo61luh', 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6asU049doNupkVllo61luh', 'duration_ms': 288720, 'time_signature': 3}

            subgenre_one_features.append([features["danceability"], features["energy"], features["key"], features["loudness"], features["mode"], features["speechiness"],
                                          features["acousticness"], features["instrumentalness"],  features["liveness"], features["valence"], features["tempo"],  features["duration_ms"], features["time_signature"], i["track"]["name"]])

            lf = lf + 1

    print("Total number of song previews of Sub Genre One")
    print(lf)

    # DOWNLOAD PREVIEW TRACKS FOR SUBGENRE 1
    directory_one = full_path + subgenre_one
    if os.path.isdir(directory_one):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(directory_one)

    for j in range(len(preview_urls)):
        urlretrieve(preview_urls[j], "{}/{}{}".format(directory_one,
                                                      'track{}'.format(j+1), ".mp3"))

    # GET PREVIEW URLS FOR SUBGENRE 2

    playlist_two_tracks = get_playlist_tracks(
        spotify_user_id, spotify_playlist_two)
    preview_urls = []
    subgenre_two_features = []
    lf = 0
    for z in playlist_two_tracks:

        if z["track"]["preview_url"] != None and lf < limit:
            preview_urls.append(z["track"]["preview_url"])

            track_uri = z["track"]["uri"]

            # print(z["track"]["name"])

            features = sp.audio_features(track_uri)[0]

            # Example feature: {'danceability': 0.612, 'energy': 0.476, 'key': 8, 'loudness': -8.256, 'mode': 1, 'speechiness': 0.0275, 'acousticness': 0.861, 'instrumentalness': 0.0044, 'liveness': 0.147, 'valence': 0.257, 'tempo': 118.381, 'type': 'audio_features', 'id': '6asU049doNupkVllo61luh', 'uri': 'spotify:track:6asU049doNupkVllo61luh', 'track_href': 'https://api.spotify.com/v1/tracks/6asU049doNupkVllo61luh', 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6asU049doNupkVllo61luh', 'duration_ms': 288720, 'time_signature': 3}

            subgenre_two_features.append([features["danceability"], features["energy"], features["key"], features["loudness"], features["mode"], features["speechiness"],
                                          features["acousticness"], features["instrumentalness"],  features["liveness"], features["valence"], features["tempo"],  features["duration_ms"], features["time_signature"], z["track"]["name"]])

            lf = lf + 1

    print("Total number of song previews of Sub Genre Two")
    print(lf)

    # DOWNLOAD PREVIEW TRACKS FOR SUBGENRE 1
    directory_two = full_path + subgenre_two
    if os.path.isdir(directory_two):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(directory_two)

    for k in range(len(preview_urls)):
        urlretrieve(preview_urls[k], "{}/{}{}".format(directory_two,
                                                      'track{}'.format(k+1), ".mp3"))

    # PUT AUDIO DATA + FEATURES INTO ARRAY FOR GENRE 1

    # Get Data for genre one
    raw_genre_one_data, sr = make_audio_data_array(
        directory_one, subgenre_one_features, limit)

    # Split data into training and testing data for genre 1
    genre_one_train, genre_one_test = train_test_split(raw_genre_one_data, 1)

    #  Save data in numpy format for genre 1
    genre_one_train_folder = full_path + subgenre_one + "_train/"
    if os.path.isdir(genre_one_train_folder):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(genre_one_train_folder)

    genre_one_test_folder = full_path + subgenre_one + "_test/"

    if os.path.isdir(genre_one_test_folder):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(genre_one_test_folder)

    np.save(genre_one_train_folder, genre_one_train)
    np.save(genre_one_test_folder, genre_one_test)

    # PUT AUDIO DATA + FEATURES INTO ARRAY FOR GENRE 2

    # Get Data for genre two
    raw_genre_two_data, sr = make_audio_data_array(
        directory_two, subgenre_two_features, limit)

    # split into training and testing data for genre 2
    genre_two_train, genre_two_test = train_test_split(raw_genre_two_data, 1)

    # Save data in numpy format for genre 2
    genre_two_train_folder = full_path + subgenre_two + "_train/"

    if os.path.isdir(genre_two_train_folder):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(genre_two_train_folder)

    genre_two_test_folder = full_path + subgenre_two + "_test/"

    if os.path.isdir(genre_two_test_folder):
        print("Folder Already Exists")
    else:
        print("Making New Folder")
        os.mkdir(genre_two_test_folder)

    np.save(genre_two_train_folder, genre_two_train)
    np.save(genre_two_test_folder, genre_two_test)
