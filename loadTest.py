import numpy as np

if __name__ == "__main__":

    dp_test = np.load("./dreampop_test/dreampop.npy", allow_pickle=True)

    # Full shape of test data
    print(dp_test.shape)
    # Shape (9,2)
    # (9 songs, 2 wide (ie 1 side is mp3 data, other side is Spotify features))
    # One song was dropped from 10 since it was less than 30 seconds (you might notice total numbers drop hence why I mention this)

    # First Song
    first_song = dp_test[0]
    # Shape: (2,)
    print(first_song.shape)
    # All songs have this shape. 1st side is mp3 data, 2nd side is spotify features

    # First Song MP3 Data
    first_song_mp3 = dp_test[0][0]
    # Shape: (662076,)
    print(np.array(first_song_mp3).shape)
    # This is the exact length of a mp3 30 second sample
    # All songs are exactly this length.
    # The raw data in in a python list format, so you might have to make it a numpy array as follows:
    # mp3_data_test_song_one = np.array(dp_test[0][0])

    # First Song spotify feature Data
    first_song_spotify_features = dp_test[0][1]
    # Shape: (14,)
    print(np.array(first_song_spotify_features).shape)
    # These are the 14 spotify features
    # WARNING: The last feature is the song name which you probably would want to remove from the data!
