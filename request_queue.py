from datetime import datetime

class CommentQueue():
    def __init__(self):
        # Initiates comment queue
        self.commentsQueue = {}
        self.idCounter = 0

    # Generates a new unique ID for the queue objects
    def newID(self):
        self.idCounter += 1
        return str(self.idCounter)

    '''
    Method to add new object to queue.
    Items must have a ID item available via the [] operation
    '''
    def addComment(self, commentObject):
        # Adds comment object to queue
        self.commentsQueue[commentObject["ID"]] = commentObject

    '''
    Makes objects available via keys by using pythons [] operation
    Also updates last updated to mark object as active
    '''
    def __getitem__(self, key):
        # Updates last interation time stamp
        self.commentsQueue[key]["lastInteraction"] = str(datetime.utcnow().isoformat())

        # Returns comment object
        return self.commentsQueue[key]
