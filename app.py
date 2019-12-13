from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime

'''
Author: La Fon, Noah
Date Created: Dec 6, 2019
References:
 - https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3
 - https://flask-restful.readthedocs.io/en/latest/index.html
'''

# Initiates flask app and creates api object for this app
app = Flask(__name__)
api = Api(app)

'''
Comments queue for storing comments before and after being processed

Example format for comment object:
{
    "ID": "1",
    "created": 2019-12-06 15:31:24.800545,
    "status": "unprocessed",
    "text": "Hey! How are you doing?",
    "result": None
}

TODO: Create script to delete old comment objects when
they have been in the queue for more than a given date
so that they don't pile up in memory. If we decide to use
a database this won't be needed.

TODO: Add documentation for API requests.
'''
commentsQueue = []

'''
TODO: We connect whatever we develope here.
This is just a placeholder and we will
need to import the method we develope.
'''
def processComment(commentID):
    # Does backend stuff...
    print("Doing backend stuff on comment:", commentID)
    return commentID

'''
Keeps track of comment IDs
Will need a better solution if we decide to
connect the system to a database.
'''
commentsIDCounter = 0
def getNewID():
    global commentsIDCounter
    commentsIDCounter += 1
    return str(commentsIDCounter)

'''
CommentAPI class for POSTing and GETting comment object.
'''
class CommentAPI(Resource):
    '''
    POST method for creating new comment instance.

    Note: commentID for this request is ignored when made
        as a comment ID will just be generated for the new object.
        I would reccomend using the text 'new' in place of the ID
        so you can visually see what kind of request it is.
    '''
    def post(self, commentID):
        # TODO: Test to see if we need to add handling for bad requests

        # Parses comment text from request
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        args = parser.parse_args()

        # Generate new comment ID
        newID = getNewID()

        # TODO: Change time format to ISO 8601
        # TODO: Change time zone to UTC
        # TODO: Add time stamp for last time object was updated

        # Fills out new comment object
        commentObject = {
            "ID": newID,
            "created": str(datetime.now()),
            "status": "unprocessed",
            "text": args["text"],
            "result": None,
        }

        # Adds comment to queue for processing
        commentsQueue.append(commentObject)

        # TODO: Make this spawn a seccond process rather than needing
        # to wait for results here?
        processComment(newID)

        # Returns new comment object
        # Front end can now extract commnetID and
        # use it to retrieve the results
        # Returns with code 201 (object created code)
        return commentObject, 201

    '''
    GET method for retrieving the results on a given comment ID.
    Returns 404 response if ID can't be found.
    '''
    def get(self, commentID):
        # Returns the comment object with the given
        # commentID if it exists.
        for commentObject in commentsQueue:
            if(commentID == commentObject["ID"]):
                # ID found, return with code 200 (OK status)
                return commentObject, 200

        # If a comment could not be found with the given ID,
        # throw a 404 error.
        return "Comment not found", 404

# Adds CommentAPI to flask app under path /comment/commentID
api.add_resource(CommentAPI, "/comment/<string:commentID>")

# Sets debug mode to true for development purposes
app.run(debug=True)
