import nltk
from nltk.corpus import webtext

import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, Dropout, TimeDistributed
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.optimizers import RMSprop
import matplotlib.pyplot as pyplot
import pickle
import sys
import heapq
import seaborn as sns
from pylab import rcParams

if __name__ == "__main__":
    '''
    Train the model

    This model is derived from Venelin Volkov's work:
    https://medium.com/@curiousily/making-a-predictive-keyboard-using-recurrent-neural-networks-tensorflow-for-hackers-part-v-3f238d824218
    '''

    nltk.download('webtext')
    text = webtext.raw()
    print('corpus length:', len(text))

    # Set up conversion between one-hot vectors and chars
    chars = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    print(f'unique chars: {len(chars)}')

    SEQUENCE_LENGTH = 40 # num of chars we input
                        # may want to change - what about before user
                        # has typed 40 chars? Do we use ngram model then?
    step = 3 # gap between inputs
    sentences = []
    next_chars = []