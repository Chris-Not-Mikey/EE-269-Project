# KNN Classification script
import os
import numpy as np
import librosa.feature
import math
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

if __name__ == "__main__": 
    # Read in audio data
    subgenre1_train_dir = '/home/christophercalloway216/EE-269-Project/dreampop_train/'
    subgenre1_test_dir = '/home/christophercalloway216/EE-269-Project/dreampop_test/'
    subgenre2_train_dir = '/home/christophercalloway216/EE-269-Project/shoegaze_train/'
    subgenre2_test_dir = '/home/christophercalloway216/EE-269-Project/shoegaze_test/'
    # dreampop_train = np.load('dreampop_train/dreampop_train.npy', allow_pickle=True)  # Old storage method
    # dreampop_test = np.load('dreampop_test/dreampop_test.npy', allow_pickle=True)
    # shoegaze_train = np.load('shoegaze_train/shoegaze_train.npy', allow_pickle=True)
    # shoegaze_test = np.load('shoegaze_test/shoegaze_test.npy', allow_pickle=True)

    # Used for preallocating size for arrays
    n_subgenre2train = len([f for f in os.listdir(subgenre2_train_dir) if f.endswith('.npy')])
    n_subgenre2test = len([f for f in os.listdir(subgenre2_test_dir) if f.endswith('.npy')])
    n_subgenre1train = len([f for f in os.listdir(subgenre1_train_dir) if f.endswith('.npy')])
    n_subgenre1test = len([f for f in os.listdir(subgenre1_test_dir) if f.endswith('.npy')])

    # Create label arrays - Assign 1 to dreampop, 0 to shoegaze
    # Y_train = np.concatenate((np.zeros((n_subgenre2train, 1)), np.ones((n_subgenre1train, 1))))
    # Y_test = np.concatenate((np.zeros((n_subgenre2test, 1)), np.ones((n_subgenre1test, 1))))

    # Perform any data preprocessing here
    # Convert to MFCC
    X_train_mfcc = []
    x_train_empty = True
    n = 0 
    # Go through shoegaze training data
    for filename in os.listdir(subgenre2_train_dir): 
        if filename.endswith('.npy'): 
            # Open file
            audiodata = np.load(os.path.join(subgenre2_train_dir, filename), allow_pickle=True)
            # Get MFCC coefficients
            if len(audiodata[0]) > 1000:  # Checks to make sure file has a valid sample
                mfcc_coeffs = librosa.feature.mfcc(np.array(audiodata[0]), sr=22050, n_mfcc=16, hop_length=512, win_length=2048)
                #mfcc_coeffs = librosa.feature.mfcc(shoegaze_train[n], sr=44100, n_mfcc=16, hop_length=16, win_length=32)
                if x_train_empty:  # If empty, creates array to store all MFCC data
                    X_train_mfcc = np.zeros((n_subgenre2train + n_subgenre1train, mfcc_coeffs.size))
                    x_train_empty = False
                X_train_mfcc[n, :] = mfcc_coeffs.flatten('F')
                n = n + 1
    Y1 = np.zeros((n, 1))
    n0 = n 
    # Go through dreampop training data
    for filename in os.listdir(subgenre1_train_dir): 
        if filename.endswith('.npy'): 
            audiodata = np.load(os.path.join(subgenre1_train_dir, filename), allow_pickle=True)
            if len(audiodata[0]) > 1000: 
                mfcc_coeffs = librosa.feature.mfcc(np.array(audiodata[0]), sr=22050, n_mfcc=16, hop_length=512, win_length=2048)
                #mfcc_coeffs = librosa.feature.mfcc(dreampop_train[n], sr=44100, n_mfcc=16, hop_length=16, win_length=32)
                X_train_mfcc[n, :] = mfcc_coeffs.flatten('F')
                n = n + 1
    Y_train = np.concatenate((Y1, np.ones((n - n0, 1))))

    if n < (n_subgenre2train + n_subgenre1train):
        X_train_mfcc = X_train_mfcc[0:n, :]
        
    # Go through test data
    n = 0
    X_test_mfcc = np.zeros((n_subgenre2test + n_subgenre1test, mfcc_coeffs.size))
    for filename in os.listdir(subgenre2_test_dir): 
        if filename.endswith('.npy'): 
            audiodata = np.load(os.path.join(subgenre2_test_dir, filename), allow_pickle=True)
            if len(audiodata[0]) > 1000: 
                mfcc_coeffs = librosa.feature.mfcc(np.array(audiodata[0]), sr=22050, n_mfcc=16, hop_length=512, win_length=2048)
                #mfcc_coeffs = librosa.feature.mfcc(shoegaze_test[n], sr=44100, n_mfcc=16, hop_length=16, win_length=32)
                X_test_mfcc[n, :] = mfcc_coeffs.flatten('F')
                n = n + 1
    Y1 = np.zeros((n, 1))
    n0 = n
    for filename in os.listdir(subgenre1_test_dir):  
        if filename.endswith('.npy'): 
            audiodata = np.load(os.path.join(subgenre1_test_dir, filename), allow_pickle=True)
            if len(audiodata[0]) > 1000: 
                mfcc_coeffs = librosa.feature.mfcc(np.array(audiodata[0]), sr=22050, n_mfcc=16, hop_length=512, win_length=2048)
                #mfcc_coeffs = librosa.feature.mfcc(dreampop_test[n], sr=44100, n_mfcc=16, hop_length=16, win_length=32)
                X_test_mfcc[n, :] = mfcc_coeffs.flatten('F')
                n = n + 1
    Y_test = np.concatenate((Y1, np.ones((n - n0, 1))))
    if n < (n_subgenre2test + n_subgenre1test): 
        X_test_mfcc = X_test_mfcc[0:n, :]


    # Apply PCA
    num_components = list(range(16, 20, 1))
    num_neighbors = list(range(2, 30, 1))
    test_acc_all = np.zeros((len(num_components), len(num_neighbors)))
    plt.figure()  # Plot test accuracies
    for pca_ind, n_c in enumerate(num_components): 
        pca = PCA(n_components=n_c)
        X_train_pca = pca.fit_transform(X_train_mfcc)
        X_test_pca = pca.transform(X_test_mfcc)

        # Test out KNN classifier accuracy
        for knn_ind, N in enumerate(num_neighbors): 
            knnclassifier = KNeighborsClassifier(n_neighbors=N)

            # Set training data
            knnclassifier.fit(X_train_pca, np.ravel(Y_train))

            # Evaluate accuracy
            # train_acc = knnclassifier.score(X_train_pca, np.ravel(Y_train))
            test_acc = knnclassifier.score(X_test_pca, np.ravel(Y_test))
            # print(train_acc)
            print(test_acc)
            # Store test accuracy
            test_acc_all[pca_ind, knn_ind] = test_acc

        print('------')

        # Plot test accuracies
        plt.plot(np.array(num_neighbors), test_acc_all[pca_ind, :], label='{} principal components'.format(n_c))
    
    # Finish plot
    plt.legend()
    plt.xlabel('Number of Nearest Neighbors')
    plt.ylabel('Accuracy')
    plt.title('Accuracy as Number of Principal Components and Nearest Neighbors Vary')
    plt.savefig('acc_plot.png')