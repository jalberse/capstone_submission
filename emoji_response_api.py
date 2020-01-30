#!/usr/bin/env python
"""
#==========================================================================
# PURPOSE:
#   An emoji response API to provide REST access to our emoji response
#
# NOTES:
#   Only tested on Python3.7
#
# USAGE:
#   $ python3.7 emojiresponse.py
#
#   Upon running this command in the appropriate environment, the API will
#   be made available on the default port of 5000.
#   Requests can be made locally as follows:
#       Creating Object:
#           A multipart form POST to http://localhost:5000/emojiresponse/new
#           with values {"text":"comment"}
#
#       Requesting Object:
#           Simply get http://localhost:5000/emojiresponse/<ID>
#           where <ID> is the ID that was given when the object was created
#==========================================================================
"""
__author__ = "lafon@ou.edu"
__date__ = "2019-01-29"
__version__ = "1.0"

from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from request_queue import CommentQueue
from quick_response import TextAnalyzer

'''
CommentAPI class for POSTing and GETting comment object.
'''
class EmojiResponseAPI(Resource):
    '''
    POST method for creating new comment instance.
    '''
    def post(self, commentID):
        # Parses comment text from request
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        args = parser.parse_args()

        # Generate new comment ID
        newID = commentQueue.newID()

        # Fills out new comment object
        commentObject = {
            "ID": newID,
            "created": str(datetime.utcnow().isoformat()),
            "lastInteraction": str(datetime.utcnow().isoformat()),
            "status": "unprocessed",
            "text": args["text"],
            "response": None,
        }

        # Adds comment to queue for processing
        commentQueue.addComment(commentObject)

        # Processes text and sets response
        commentObject["response"] = analyzer.get_text_response(args["text"])

        # Returns new comment object
        # with code 201 (object created code)
        return commentObject, 201

    '''
    GET method for retrieving the results on a given comment ID.
    Returns 404 response if ID can't be found.
    '''
    def get(self, commentID):
        # Returns the comment object with the given
        # commentID if it exists.
        try:
            # ID found, return with code 200 (OK status)
            return commentQueue[commentID], 200
        except KeyError:
            # If a comment could not be found with the given ID,
            # throw a 404 error.
            return "Comment not found", 404


if __name__ == '__main__':
    # Initiates flask app and creates api object for this app
    app = Flask(__name__)
    api = Api(app)

    # Gives app appropriate context
    with app.app_context():
        analyzer = TextAnalyzer()
        commentQueue = CommentQueue()

    # Adds CommentAPI to flask app under path /emojiresponse/commentID
    api.add_resource(EmojiResponseAPI, "/emojiresponse/<string:commentID>")

    # Sets debug mode to true for development purposes
    app.run(debug=True)
