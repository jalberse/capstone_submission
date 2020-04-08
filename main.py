from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from quick_response import TextAnalyzer
from request_queue import CommentQueue

from emoji_response_api import EmojiResponseAPI
from text_response_api import TextResponseAPI

if __name__ == '__main__':
    
    # Initiates flask app and creates api object for this app
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    
    # app = Flask(__name__)
    
    # Gives app appropriate context
    with app.app_context():
        analyzer = TextAnalyzer()
        commentQueue = CommentQueue()
    
    # Adds CommentAPI to flask app under path /textresponse/commentID
    api.add_resource(TextResponseAPI, "/textresponse/<string:commentID>")
    
    # Adds CommentAPI to flask app under path /emojiresponse/commentID
    api.add_resource(EmojiResponseAPI, "/emojiresponse/<string:commentID>")
    
    # Sets debug mode to true for development purposes
    app.run(debug=True)
    