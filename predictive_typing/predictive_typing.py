import nltk
from nltk.corpus import webtext
from nltk.corpus import gutenberg

import os
import numpy as np
import tensorflow as tf

os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # Disable GPU training - uncomment to allow GPU training. 

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, Dropout, TimeDistributed
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import pickle
import sys
import heapq
from pylab import rcParams

#TODO Test refactor
#TODO train on a larger, web-based corpus. For now, Jane Austen
    #TODO only feasibly once have GPU support :(

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

        physical_devices = tf.config.list_physical_devices('GPU') 
        try: 
          tf.config.experimental.set_memory_growth(physical_devices[0], True) 
        except: 
          # Invalid device or cannot modify virtual devices once initialized. 
          pass 

        self.SEQUENCE_LENGTH = sequence_length
        self.text = text
        self.chars = sorted(list(set(self.text)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

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
                self.history = pickle.load(open("history.p", "rb"))
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
        x = np.zeros((len(xs), self.SEQUENCE_LENGTH, len(self.chars)), dtype=np.bool)
        y = np.zeros((len(xs), len(self.chars)), dtype=np.bool)

        # For each example i...
        for i, sentence in enumerate(xs):
            # For the t'th char, encode a one-hot vector
            for t, char in enumerate(sentence):
                x[i, t, self.char_indices[char]] = 1
            # For the target char, encode the one-hot output
            y[i, self.char_indices[ys[i]]] = 1

        # TODO: Hyperparamter testing
        model = Sequential()
        model.add(LSTM(128, input_shape=(self.SEQUENCE_LENGTH, len(self.chars))))
        model.add(Dense(len(self.chars)))
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
        # Transforms text into sequence of one-hot vectors
        x = np.zeros((1, self.SEQUENCE_LENGTH, len(self.chars)))
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
        while True:
            # predict the next char
            x = self._preprocess_text(text)
            preds = self.model.predict(x, verbose=0)[0]
            next_index = self._sample(preds, top_n=1)[0]
            next_char = self.indices_char[next_index]
            
            # next we predict last 40 included predicted char
            text = text[1:] + next_char
            completion += next_char

            if next_char in stop:
                return completion

    def predict_completions(self, text, stop=[' '], n=3):
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

    # Test predictive capability
    test_set = [
        "There is nothing I would not do for those who are really my friends. I have no notion of loving people by halves, it is not my nature.",
        "There is a stubbornness about me that never can bear to be frightened at the will of others. My courage always rises at every attempt to intimidate me.",
        "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
        "Vanity and pride are different things, though the words are often used synonymously. A person may be proud without being vain. Pride relates more to our opinion of ourselves, vanity to what we would have others think of us.",
    ]
    
    nltk.download('gutenberg')
    text = gutenberg.raw('austen-emma.txt').lower()

    tp = text_predictor(text)
    history = tp.fit()

    # Plot training
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    