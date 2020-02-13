import nltk
from nltk.corpus import webtext_raw

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
    webtext_raw = webtext.raw()