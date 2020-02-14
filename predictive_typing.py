import nltk
from nltk.corpus import webtext
from nltk.corpus import gutenberg

import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, Dropout, TimeDistributed
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import pickle
import sys
import heapq
from pylab import rcParams

if __name__ == "__main__":
    '''
    Train the model

    This model is based on Venelin Volkov's work:
    https://medium.com/@curiousily/making-a-predictive-keyboard-using-recurrent-neural-networks-tensorflow-for-hackers-part-v-3f238d824218
    '''

    nltk.download('webtext')
    text = webtext.raw().lower()

    print('corpus length:', len(text))

    # Set up conversion between one-hot vectors and chars
    chars = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    print(f'unique chars: {len(chars)}')

    exit()

    # Extract training data from text
    SEQUENCE_LENGTH = 40 # num of chars we input
                        # may want to change - what about before user
                        # has typed 40 chars? Do we use ngram model then?
    step = 3 # gap between inputs
    xs = [] # RNN input. Last SEQUENCE_LENGTH characters
    ys = [] # RNN target. The 41st char
    for i in range(0, len(text) - SEQUENCE_LENGTH, step):
        xs.append(text[i: i + SEQUENCE_LENGTH])
        ys.append(text[i + SEQUENCE_LENGTH])

    # Place examples in single data structure
    x = np.zeros((len(xs), SEQUENCE_LENGTH, len(chars)), dtype=np.bool)
    y = np.zeros((len(xs), len(chars)), dtype=np.bool)

    # For each example i...
    for i, sentence in enumerate(xs):
        # For the t'th char, encode a one-hot vector
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        # For the target char, encode the one-hot output
        y[i, char_indices[ys[i]]] = 1

    print('input matrix')
    print('(Number training examples, input size, number unique chars)')
    print(x.shape)
    print('target matrix')
    print('(Number training examples, number unique chars)')
    print(y.shape)

    print(chars)

    # Make and train the model
    # TODO: Hyperparamter testing
    model = Sequential()
    model.add(LSTM(128, input_shape=(SEQUENCE_LENGTH, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    history = model.fit(x, y, validation_split=0.05, batch_size=128, epochs=20, shuffle=True).history

    # Save model
    model.save('keras_model.h5')
    pickle.dump(history, open("history.p", "wb"))

    # Load model (TODO remove just making sure it saves right)
    model = load_model('keras_model.h5')
    history = pickle.load(open("history.p", "rb"))

    # Plot training
    plt.plot(history['acc'])
    plt.plot(history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    