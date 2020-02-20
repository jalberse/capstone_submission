#!/usr/bin/env python
"""
#==========================================================================
# PURPOSE:
#   A predictive typing API to get the next string of characters the user
#   is likely to type.
#
# NOTES:
#   Only tested on Python3.7
#
# REFERENCES:
#   https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3
#   https://flask-restful.readthedocs.io/en/latest/index.html
#
# USAGE:
#  $ python3.7 predictive_typing_api.py
# 
#   Upon running this command in the appropriate environment, the API will
#   be made available on the default port of 5000.
#   You can now try to predict the next thing a user might type on a string
#   of up to SEQUENCE_LENGTH (usually 40) characters. Sending more than
#   SEQUENCE_LENGTH characters will just truncate the string to the last 
#   SEQUENCE_LENGTH characters.
#   
#   It is not advised to try and predict the next characters on a string
#   less than 2 words.
#   
#   Requests can be made locally as follows:
#       Creating Object:
#           A multipart form POST to http://localhost:5000/predicttext
#           with values {"text": "string of user typed cahracters"}
#==========================================================================
"""
__author__ = "lafon@ou.edu"
__date__ = "2019-01-29"
__version__ = "1.0"

from flask import Flask
from flask_restful import Api, Resource, reqparse

import nltk
from predictive_typing.predictive_typing import text_predictor
from nltk.corpus import gutenberg

import os
from os.path import join

'''
CommentAPI class for GETting a string of characters
that may be what the user is going to type next.
'''
class PredictiveTextAPI(Resource):
    '''
    GET method for getting a string of characters
    that the user may intend to type next.
    '''
    def get(self):
        # Parses comment text from request
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        args = parser.parse_args()
        text = args["text"]

        # Formats text
        text = text.lower()
        if len(text) < textPredictor.SEQUENCE_LENGTH:
            # Text needs padding

            # Pads sequence of characters with spaces if it is
            # shorter than SEQUENCE_LENGTH
            text = (textPredictor.SEQUENCE_LENGTH - len(text)) * " " + text
        else:
            # Text needs truncating

            # Grads last SEQUENCE_LENGTH worth of characters truncating
            # any extra at the start.
            text = text[len(text) - textPredictor.SEQUENCE_LENGTH:len(text)]

        # Makes prediction
        textResult = tp.predict_completions(text,n=3)

        # Returns predicted string of characters
        # with code 200 (ok code)
        return textResult, 200

if __name__ == '__main__':
    # Initiates flask app and creates api object for this app
    app = Flask(__name__)
    api = Api(app)

    # Initializes text predictor for API context
    nltk.download('gutenberg')
    text = gutenberg.raw('austen-emma.txt').lower()

    # Loads model for predictive typing
    tp =  text_predictor(text, model_filename=join(os.getcwd(), 'predictive_typing', 'test_model.h5'), history_filename=join(os.getcwd(), 'predictive_typing', 'test_history.p'))

    # Gives app appropriate context
    with app.app_context():
        textPredictor = tp

    # Configures app for running
    api.add_resource(PredictiveTextAPI, "/predicttext")

    # Sets debug mode to true for development purposes
    app.run(debug=True)
