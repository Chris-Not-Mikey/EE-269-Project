import librosa
import os
import numpy as np


# Take in a directory and loads all the mp3 data

SONG_LENGTH = 662076


def make_audio_data_array(folder):
    data = []

    sr = 0
    counter = 0
    print(folder)
    for filename in os.listdir(folder):

        if filename.endswith(".mp3"):

            path = folder + "/" + filename
            y, sr = librosa.load(path)
            sr_out = sr

            # Reject all songs shorter than 30 seconds
            if len(y) < SONG_LENGTH:
                continue
            data.append(list(y[0:SONG_LENGTH]))

            continue
        else:
            continue

    output = np.array(data)

    return output, sr

# Takes in a numpy array and splits it randomply into training and testing data


def train_test_split(data, split_index):

    np.random.shuffle(data)
    training, test = data[:split_index, :], data[split_index:, :]

    return training, test
