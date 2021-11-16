import librosa
import os
import numpy as np


# Take in a directory and loads all the mp3 data

# We only allow songs to be exactly 30 seconds
SONG_LENGTH = 662076


def make_audio_data_array(folder, features, limit):
    data = []

    sr = 0
    counter = 0

    for filename in os.listdir(folder):

        if counter == limit:
            continue

        # go in order of the tracks: 1,2,3,....
        file_string = "track" + str(counter+1) + ".mp3"
        path = folder + "/" + file_string

        if os.path.isfile(path):
            print(path)

           # path = folder + "/" + filename
            y, sr = librosa.load(path)

            # Reject all songs shorter than 30 seconds
            if len(y) < SONG_LENGTH:
                counter = counter + 1
                continue

            # Merge audio data and track features into big array
            all_features = [list(y[0:SONG_LENGTH]), features[counter]]

            data.append(all_features)

            counter = counter + 1

            continue
        else:
            counter = counter + 1
            continue

    output = np.array(data, dtype=object)

    return output, sr

# Takes in a numpy array and splits it randomly into training and testing data


def train_test_split(data, split_index):

    np.random.shuffle(data)
    training, test = data[:split_index, :], data[split_index:, :]

    return training, test
