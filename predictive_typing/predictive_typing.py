import nltk
from nltk.corpus import webtext
from nltk.corpus import gutenberg

import os
import numpy as np
import tensorflow as tf
from collections import defaultdict

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, Dropout, TimeDistributed
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import pickle
import sys
import heapq
from pylab import rcParams

# TODO train on a larger, web-based corpus. For now, Jane Austen
# TODO better way of loading models? Low priority

class text_predictor:
    '''
    A model for autocomplete and text prediction using an LSTM network.

    Usage:
    1)
    a) With a pretrained model:
        Simply initialize text_predictor with the model filename and history filename to load the model in.
        Ensure that text and sequence_length match the parameters used to train the model originally.

    b) To train a new model:
        Initialize the model
        use fit() to train the model. This function returns the keras training history if you wish to graph it.
        
    2) Call predict_completions() to return a list of n autocompletes provided the given stop chars.

    This model is based on Venelin Volkov's work:
    https://medium.com/@curiousily/making-a-predictive-keyboard-using-recurrent-neural-networks-tensorflow-for-hackers-part-v-3f238d824218
    '''
    def __init__(self, text, sequence_length=40, model_filename=None, history_filename=None):
        '''
        @text the text to train the model on, or the text the model was trained on. 
                Recommend calling .lower() on text before passing in.
                Even if loading model in, must know original text to derive char data.
        @sequence_length the model will predict the next character based on the last sequence_length chars
                        If loading a model, ensure this matches the sequence length used when training it
        @model_filename If not specified, untrained model will be initialized.
                        If specified, the model will be loaded from the filename. 
        @history_filename If not specified, left as None and updated when model is trained.
                        If specified, loads training history in for plotting. File is pickled keras history object. 
        '''

        self.SEQUENCE_LENGTH = sequence_length
        self.text = text
        self.chars = sorted(list(set(self.text)))
        self.char_indices = defaultdict(lambda: 0, ((c, i+1) for i, c in enumerate(self.chars)))
        print(self.char_indices)
        self.indices_char = defaultdict(lambda: '', ((i+1, c) for i, c in enumerate(self.chars)))
        print(self.indices_char)

        if model_filename:
            # Load model in if file provided
            try:
                self.model = load_model(model_filename)
            except OSError:
                print(f'Could not load file {model_filename}')
        else:
            # Else prepare model for training
            self.model, self.x, self.y = self._prepare_model()            
        
        if history_filename:
            try:
                self.history = pickle.load(open(history_filename, "rb"))
            except OSError:
                print(f'Could not load file {history_filename}')
        else:
            self.history = None

    def _prepare_model(self):
        '''
        Helper function for constructor
        Compiles model and formats training data
        '''
        # Extract training data from text
        step = 3 # gap between inputs
        xs = [] # RNN input. Last SEQUENCE_LENGTH characters
        ys = [] # RNN target. The 41st char
        for i in range(0, len(text) - self.SEQUENCE_LENGTH, step):
            xs.append(self.text[i: i + self.SEQUENCE_LENGTH])
            ys.append(self.text[i + self.SEQUENCE_LENGTH])

        # Place examples in single data structure
        x = np.zeros((len(xs), self.SEQUENCE_LENGTH, len(self.chars) + 1), dtype=np.bool)
        y = np.zeros((len(xs), len(self.chars) + 1), dtype=np.bool)

        # For each example i...
        for i, sentence in enumerate(xs):
            # For the t'th char, encode a one-hot vector
            for t, char in enumerate(sentence):
                x[i, t, self.char_indices[char]] = 1
            # For the target char, encode the one-hot output if the target is in char set
            y[i, self.char_indices[ys[i]]] = 1

        # TODO: Hyperparamter testing
        model = Sequential()
        model.add(LSTM(128, input_shape=(self.SEQUENCE_LENGTH, len(self.chars) + 1)))
        model.add(Dense(len(self.chars) + 1))
        model.add(Activation('softmax'))

        optimizer = RMSprop(lr=0.01)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model, x, y

    def fit(self, validation_split=0.05, batch_size=128, epochs=20, verbose=1, shuffle=True):
        self.history = self.model.fit(self.x, self.y, validation_split=validation_split, batch_size=batch_size, epochs=epochs, verbose=verbose, shuffle=shuffle).history
        return self.history

    def save_model(self, filename):
        self.model.save(filename)

    def save_history(self, filename):
        pickle.dump(self.history, open(filename, "wb"))

    def _preprocess_text(self, text):
        # Formats text
        text = list(text[-self.SEQUENCE_LENGTH:].lower())
        # Places empty string elements to pad front, in case text shorter that SEQUENCE_LENGTH
        text = [''] * (self.SEQUENCE_LENGTH - len(text)) + text

        # Transforms text into sequence of one-hot vectors
        x = np.zeros((1, self.SEQUENCE_LENGTH, len(self.chars) + 1))
        for t, char in enumerate(text):
            x[0, t, self.char_indices[char]] = 1.
        return x

    def _sample(self, preds, top_n=3):
        preds = np.asarray(preds).astype('float64')
        preds = preds / np.sum(preds)
        return heapq.nlargest(top_n, range(len(preds)), preds.take)

    def _predict_text(self, text, stop=[' ']):
        '''
        Predicts text until one of the characters in stop are encountered
        By default will autocomplete one word, or else the next word
        if the input text end with a space.

        Pass punctuation to predict until the end of a sentence.

        Returns the predicted next letters until stop. 
        '''
        orig_text = text
        completion = '' #tracks what chars we're appending
        predicted_cnt = 0
        while True:
            # predict the next char
            x = self._preprocess_text(text)
            preds = self.model.predict(x, verbose=0)[0]
            next_index = self._sample(preds, top_n=1)[0]
            next_char = self.indices_char[next_index]
            
            # next we predict last 40 included predicted char
            text = text[1:] + next_char
            completion += next_char
            predicted_cnt += 1
            
            # TODO is there a better way to stop if we are looping w/out hitting a stop char?
            if next_char in stop or predicted_cnt >= 30: 
                return completion

    def predict_completions(self, text, stop=[' ','\n'], n=3):
        '''
        Returns n possible autocompletes
        '''
        x = self._preprocess_text(text)
        preds = self.model.predict(x, verbose=0)[0]
        next_indices = self._sample(preds, n)
        return [self.indices_char[idx] + self._predict_text(text[1:] + self.indices_char[idx], stop=stop) for idx in next_indices]

if __name__ == "__main__":
    '''
    Example for how to use the model
    '''

    # TODO Use customer support dataset (will require some cleaning)
    # TODO Hyperparameter tuning
    # TODO example on how to verify output in

    # Test predictive capability
    test_set = [
        "There is nothing I would not do for those who are really my friends. ",
        "There is a stubbornness abo",
        "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a w",
        "Vanity and pride are differ",
        "hi",
        "#",
    ]
    
    nltk.download('gutenberg')
    text = gutenberg.raw('austen-emma.txt').lower()

    # How to train a model

    #tp = text_predictor(text)
    #history = tp.fit()
    #tp.save_model('gpu-test_model.h5')
    #tp.save_history('gpu-test_history.p')

    # test loading model
    tp = text_predictor(text, model_filename='gpu-test_model.h5', history_filename='gpu-test_history.p')
    history = tp.history

    # Test using model
    for test in test_set:
        print(test)
        print(tp.predict_completions(test,n=5)) # can pass stop=['.'] e.g. to predict till sentences (liable to hang/break)

    # Plot training
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('gpu-test_accuracy.png')
    plt.clf()

    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('gpu-test_loss.png')


    